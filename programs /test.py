#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from pathlib import Path
import gradebook as operations
import unittest


class TestStudentDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up for class"""
        print("start testing the gradebook")
        print("==========")

    @classmethod
    def tearDownClass(cls):
        """Tear down for class"""
        print(" succesfully")
        print("==========")
        print("end of testing\n")
    
    def setUp(self):
        self.store_tests = Path("for_tests.db")

    def tearDown(self):
        if self.store_tests.exists():
            conn = sqlite3.connect(self.store_tests)
            conn.close()
            self.store_tests.unlink()

    def test_create_db(self):
        '''Тестирование создания базы данных.'''
        operations.create_db(self.store_tests)

        conn = sqlite3.connect(self.store_tests)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall() 
        self.assertIn(('groups',), tables)
        self.assertIn(('students',), tables)
        conn.close() 


class Check_student(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("start testing adding test")
        print("==========")

    @classmethod
    def tearDownClass(cls):
        '''Вызывается один раз для всего класса, в конце.'''
        print(" succesfully")
        print("==========")
        print("tests finished\n")

    def setUp(self):
        self.store_tests = Path("test_add.db")

    def tearDown(self):
        '''Метод tearDown вызывается после каждого теста для очистки окружения.
        В данном случае он избавляется от временной базы данных после проведения тестов.'''
        if self.store_tests.exists():
            conn = sqlite3.connect(self.store_tests)
            conn.close()
            self.store_tests.unlink()

    def test_add_student(self):
        '''Попытка добавления нового человека.'''
        operations.create_db(self.store_tests)
        operations.add_student(self.store_tests, "A",
                             "1", [1, 2, 3, 4, 5])

        conn = sqlite3.connect(self.store_tests)
        cursor = conn.cursor()
        # Запрос. Сначала получение всех 4-ёх параметров, после чего относительно group_i
        # из таблицы groups, вставляются (Правильнее сказать соединяются) фамилии в таблицу test.
        cursor.execute(
            """
            SELECT students.student_name, groups.group_number, students.performance
            FROM students
            INNER JOIN groups ON groups.group_id = students.group_id
            """
        )
        student = cursor.fetchone()
        # Проверка на не пустоту, после чего поэлементная проверка содержимого на правильность.
        self.assertIsNotNone(student)
        self.assertEqual(student[0], "A")
        self.assertEqual(student[1], "1")
        self.assertEqual(list(map(int, student[2].split(','))), [1, 2, 3, 4, 5])

        conn.close()


class Check_All_Selecting(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("start testing all select test")
        print("==========")

    @classmethod
    def tearDownClass(cls):
        '''Вызывается один раз для всего класса, в конце.'''
        print(" succesfully")
        print("==========")
        print("tests finished\n")

    def setUp(self):
        self.store_tests = Path("test_all_select.db")

    def tearDown(self):
        '''Метод tearDown вызывается после каждого теста для очистки окружения.
        В данном случае он избавляется от временной базы данных после проведения тестов.'''
        if self.store_tests.exists():
            conn = sqlite3.connect(self.store_tests)
            conn.close()
            self.store_tests.unlink()

    def test_select_all(self):
        '''Попытка получения вообще всех записей о людях.'''
        operations.create_db(self.store_tests)
        # Сразу 3 записи.
        operations.add_student(self.store_tests, "A",
                             "1", [1, 2, 3, 4, 5])
        operations.add_student(self.store_tests, "B",
                             "2", [1, 2, 3, 4, 5])
        operations.add_student(self.store_tests, "C",
                             "3", [1, 2, 3, 4, 5])
        test = operations.select_all(self.store_tests)
        # Проверка, 3 ли записи получено, после чего все 3 проверяются на правильность.
        self.assertEqual(len(test), 3)
        self.assertEqual(test[0]["name"], "A")
        self.assertEqual(test[0]["group"], "1")
        self.assertEqual(test[0]["performance"], [1, 2, 3, 4, 5])
        self.assertEqual(test[1]["name"], "B")
        self.assertEqual(test[1]["group"], "2")
        self.assertEqual(test[1]["performance"], [1, 2, 3, 4, 5])
        self.assertEqual(test[2]["name"], "C")
        self.assertEqual(test[2]["group"], "3")
        self.assertEqual(test[2]["performance"], [1, 2, 3, 4, 5])


class Check_Find(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("start testing find test")
        print("==========")

    @classmethod
    def tearDownClass(cls):
        print(" succesfully")
        print("==========")
        print("tests finished\n")


    def setUp(self):
        self.store_tests = Path("test_find.db")

    def tearDown(self):
        if self.store_tests.exists():
            conn = sqlite3.connect(self.store_tests)
            conn.close()
            self.store_tests.unlink()

    def test_find(self):
        operations.create_db(self.store_tests)
        operations.add_student(self.store_tests, "A",
                             "1", [1, 2, 3, 4, 5])
        operations.add_student(self.store_tests, "B",
                             "2", [1, 1, 3, 4, 5])
        operations.add_student(self.store_tests, "C",
                             "3", [1, 2, 3, 4, 5])

        test = operations.find(self.store_tests)
        self.assertEqual(len(test), 2)
        self.assertEqual(test[0]["name"], "A")
        self.assertEqual(test[0]["group"], "1")
        self.assertEqual(test[0]["performance"], [1, 2, 3, 4, 5])

        self.assertEqual(test[1]["name"], "C")
        self.assertEqual(test[1]["group"], "3")
        self.assertEqual(test[1]["performance"], [1, 2, 3, 4, 5])


if __name__ == "__main__":
    unittest.main()
