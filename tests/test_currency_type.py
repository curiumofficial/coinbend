from unittest import TestCase

from coinbend.globals import *
from coinbend.currency_type import *
import decimal
import random
from decimal import *
import datetime
import logging

getcontext().prec = 10000
getcontext().rounding = ROUND_FLOOR

def remove_exponent(d):
    '''Remove exponent and trailing zeros.

    >>> remove_exponent(Decimal('5E+3'))
    Decimal('5000')

    '''
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()

class test_currency_type(TestCase):
    def test(self):
        #Test logical operators.
        #>, <, ==, <=, >=, !=
        c = C()
        bool_exps = [
            ("2.0", "2.0", (">", "<", "==", "<=", ">=", "!="), (0, 0, 1, 1, 1, 0)),
            ("2.0", "1.0", (">", "<", "==", "<=", ">=", "!="), (1, 0, 0, 0, 1, 1)),
            ("1.0", "2.0", (">", "<", "==", "<=", ">=", "!="), (0, 1, 0, 1, 0, 1)),
            ("2.1", "2.0", (">", "<", "==", "<=", ">=", "!="), (1, 0, 0, 0, 1, 1)),
            ("2.0", "2.1", (">", "<", "==", "<=", ">=", "!="), (0, 1, 0, 1, 0, 1)),
            ("2.0", "3.1", (">", "<", "==", "<=", ">=", "!="), (0, 1, 0, 1, 0, 1)),
            ("2.3", "3.1", (">", "<", "==", "<=", ">=", "!="), (0, 1, 0, 1, 0, 1)),
            ("3.3", "2.1", (">", "<", "==", "<=", ">=", "!="), (1, 0, 0, 0, 1, 1)),
            ("3.3", "2.6", (">", "<", "==", "<=", ">=", "!="), (1, 0, 0, 0, 1, 1)),
            ("4.3", "5.3", (">", "<", "==", "<=", ">=", "!="), (0, 1, 0, 1, 0, 1)),
            ("5.3", "4.4", (">", "<", "==", "<=", ">=", "!="), (1, 0, 0, 0, 1, 1)),
            ("2", "2", (">", "<", "==", "<=", ">=", "!="), (0, 0, 1, 1, 1, 0)),
            ("2", "3", (">", "<", "==", "<=", ">=", "!="), (0, 1, 0, 1, 0, 1)),
            ("3", "2", (">", "<", "==", "<=", ">=", "!="), (1, 0, 0, 0, 1, 1)),
            ("2.2", "2.2", (">", "<", "==", "<=", ">=", "!="), (0, 0, 1, 1, 1, 0)),
            ("2.2", "2.3", (">", "<", "==", "<=", ">=", "!="), (0, 1, 0, 1, 0, 1)),
            ("2.2", "3.2", (">", "<", "==", "<=", ">=", "!="), (0, 1, 0, 1, 0, 1)),
            ("2.2", "3.3", (">", "<", "==", "<=", ">=", "!="), (0, 1, 0, 1, 0, 1)),
            ("2.3", "2.3", (">", "<", "==", "<=", ">=", "!="), (0, 0, 1, 1, 1, 0)),
            ("2.3", "3.3", (">", "<", "==", "<=", ">=", "!="), (0, 1, 0, 1, 0, 1)),
            ("3.2", "2.2", (">", "<", "==", "<=", ">=", "!="), (1, 0, 0, 0, 1, 1)),
            ("3.2", "2.3", (">", "<", "==", "<=", ">=", "!="), (1, 0, 0, 0, 1, 1)),
            ("3.2", "3.2", (">", "<", "==", "<=", ">=", "!="), (0, 0, 1, 1, 1, 0)),
            ("3.2", "3.3", (">", "<", "==", "<=", ">=", "!="), (0, 1, 0, 1, 0, 1)),
            ("3.3", "2.2", (">", "<", "==", "<=", ">=", "!="), (1, 0, 0, 0, 1, 1)),
            ("3.3", "2.3", (">", "<", "==", "<=", ">=", "!="), (1, 0, 0, 0, 1, 1)),
            ("3.3", "3.2", (">", "<", "==", "<=", ">=", "!="), (1, 0, 0, 0, 1, 1)),
            ("3.3", "3.3", (">", "<", "==", "<=", ">=", "!="), (0, 0, 1, 1, 1, 0))
        ]

        for exp in bool_exps:
            op_a = exp[0]
            op_b = exp[1]
            operators = exp[2]
            results = exp[3]
            operator = ""
            answer = 0
            math_answer = 0
            try:
                for i in range(0, len(operators)):
                    operator = operators[i]
                    expected_result = results[i]
                    if operators[i] == ">":
                        answer = float(op_a) > float(op_b)

                    if operators[i] == "<":
                        answer = float(op_a) < float(op_b)

                    if operators[i] == "==":
                        answer = float(op_a) == float(op_b)

                    if operators[i] == "<=":
                        answer = float(op_a) <= float(op_b)

                    if operators[i] == ">=":
                        answer = float(op_a) >= float(op_b)

                    if operators[i] == "!=":
                        answer = float(op_a) != float(op_b)

                    answer = int(answer)
                    math_answer = c.math(op_a, op_b, operator)
                    if answer != expected_result:
                        print("a")
                        raise Exception
                    if answer != math_answer:
                        print("b")
                        raise Exception

            except:
                print("FAIL")
                print(str(op_a) + " " + operator + " " + str(op_b))
                print("Float answer: " + str(answer))
                print("Expected answer: " + str(expected_result))
                print("Math answer: " + str(math_answer))
                assert False

        #Note: Incremential gen would be more systematic.
        #generate = 0
        generate = 10000
        #show_success = 1
        show_success = 0
        tests = [
            ['10.001', '9.100002', '-', '0.9009980000000000'],
            ['10.001', '9.100002', '+', '19.1010020000000000'],
            ['10.001', '9.100002', '*', '91.0091200020000000'],
            ['89.90010', '10.100020', '-', '79.8000800000000000'],
            ['89.90010', '10.100020', '+', '100.0001200000000000'],
            ['89.90010', '10.100020', '*', '907.9928080020000000'],
            ['8.0010', '3.600001', '-', '4.4009990000000000'],
            ['8.0010', '3.600001', '+', '11.6010010000000000'],
            ['8.0010', '3.600001', '*', '28.8036080010000000'],
            ['3.0001', '3.0001', '-', '0.0000000000000000'],
            ['3.0001', '3.0001', '+', '6.0002000000000000'],
            ['3.0001', '3.0001', '*', '9.0006000100000000'],
            ['2.03', '2.02', '-', '0.0100000000000000'],
            ['2.03', '2.02', '+', '4.0500000000000000'],
            ['2.03', '2.02', '*', '4.1006000000000000'],
            ['5', '4', '-', '1.0000000000000000'],
            ['5', '4', '+', '9.0000000000000000'],
            ['5', '4', '*', '20.0000000000000000'],
            ['5.000010000', '4.400000100', '-', '0.6000099000000000'],
            ['5.000010000', '4.400000100', '+', '9.4000101000000000'],
            ['5.000010000', '4.400000100', '*', '22.0000445000010000'],
            ['1', '1', '-', '0.0000000000000000'],
            ['1', '1', '+', '2.0000000000000000'],
            ['1', '1', '*', '1.0000000000000000'],
            ['1', '0.0000000000000001', '-', '0.9999999999999999'],
            ['1', '0.0000000000000001', '+', '1.0000000000000001'],
            ['1', '0.0000000000000001', '*', '0.0000000000000001'],
            ['1.0000000000000000', '0.0000000000000001', '-', '0.9999999999999999'],
            ['1.0000000000000000', '0.0000000000000001', '+', '1.0000000000000001'],
            ['1.0000000000000000', '0.0000000000000001', '*', '0.0000000000000001'],
            ['1.0000000000000001', '0.9999999999999999', '-', '0.0000000000000002'],
            ['1.0000000000000001', '0.9999999999999999', '+', '2.0000000000000000'],
            ['1.0000000000000001', '0.9999999999999999', '*', '0.9999999999999999'],
            ['1.9999999999999999', '1.0000000000000001', '-', '0.9999999999999998'],
            ['1.9999999999999999', '1.0000000000000001', '+', '3.0000000000000000'],
            ['1.9999999999999999', '1.0000000000000001', '*', '2.0000000000000000'],
            ['1.0000000000000000', '0.9999999999999999', '-', '0.0000000000000001'],
            ['1.0000000000000000', '0.9999999999999999', '+', '1.9999999999999999'],
            ['1.0000000000000000', '0.9999999999999999', '*', '0.9999999999999999'],
            ['7', '3.2222', '-', '3.7778000000000000'],
            ['7', '3.2222', '+', '10.2222000000000000'],
            ['7', '3.2222', '*', '22.5554000000000000'],
            ['6.1', '4.5', '-', '1.6000000000000000'],
            ['6.1', '4.5', '+', '10.6000000000000000'],
            ['6.1', '4.5', '*', '27.4500000000000000'],
            ['6', '4.5', '-', '1.5000000000000000'],
            ['6', '4.5', '+', '10.5000000000000000'],
            ['6', '4.5', '*', '27.0000000000000000'],
            ['6.33', '4.5555', '-', '1.7745000000000000'],
            ['6.33', '4.5555', '+', '10.8855000000000000'],
            ['6.33', '4.5555', '*', '28.8363150000000000'],
            ['6', '5', '-', '1.0000000000000000'],
            ['6', '5', '+', '11.0000000000000000'],
            ['6', '5', '*', '30.0000000000000000'],
            ['633333', '4.1', '-', '633328.9000000000000000'],
            ['633333', '4.1', '+', '633337.1000000000000000'],
            ['633333', '4.1', '*', '2596665.3000000000000000'],
            ['532298073.2613150550000000', '401155464.5862338670000000', '-', '131142608.6750811880000000'],
            ['532298073.2613150550000000', '401155464.5862338670000000', '+', '933453537.8475489220000000'],
            ['532298073.2613150550000000', '401155464.5862338670000000', '*', '213534280877499992.0233405461979676'],
            ['10.1', '8.001', '-', '2.0990000000000000'],
            ['10.1', '8.001', '+', '18.1010000000000000'],
            ['10.1', '8.001', '*', '80.8101000000000000'],
            ['10.0010', '8.60001', '-', '1.4009900000000000'],
            ['10.0010', '8.60001', '+', '18.6010100000000000'],
            ['10.0010', '8.60001', '*', '86.0087000100000000'],
            ['89.100020', '10.90010', '-', '78.1999200000000000'],
            ['89.100020', '10.90010', '+', '100.0001200000000000'],
            ['89.100020', '10.90010', '*', '971.1991280020000000'],
            ['21', '10', '-', '11.0000000000000000'],
            ['21', '10', '+', '31.0000000000000000'],
            ['21', '10', '*', '210.0000000000000000'],
            ['99', '10', '-', '89.0000000000000000'],
            ['99', '10', '+', '109.0000000000000000'],
            ['99', '10', '*', '990.0000000000000000'],
            ['10', '0', '-', '10.0000000000000000'],
            ['10', '0', '+', '10.0000000000000000'],
            ['10', '0', '*', '0.0000000000000000'],
            ['0', '0', '-', '0.0000000000000000'],
            ['0', '0', '+', '0.0000000000000000'],
            ['0', '0', '*', '0.0000000000000000'],
            ['1', '0', '-', '1.0000000000000000'],
            ['1', '0', '+', '1.0000000000000000'],
            ['1', '0', '*', '0.0000000000000000'],
            ['0', '0', '-', '0.0000000000000000'],
            ['0', '0', '+', '0.0000000000000000'],
            ['0', '0', '*', '0.0000000000000000'],
            ['1', '1', '-', '0.0000000000000000'],
            ['1', '1', '+', '2.0000000000000000'],
            ['1', '1', '*', '1.0000000000000000'],
            ['0', '0.0', '-', '0.0000000000000000'],
            ['0', '0.0', '+', '0.0000000000000000'],
            ['0', '0.0', '*', '0.0000000000000000'],
            ['1', '0.0', '-', '1.0000000000000000'],
            ['1', '0.0', '+', '1.0000000000000000'],
            ['1', '0.0', '*', '0.0000000000000000'],
            ['1', '0.1', '-', '0.9000000000000000'],
            ['1', '0.1', '+', '1.1000000000000000'],
            ['1', '0.1', '*', '0.1000000000000000'],
            ['1', '1.0', '-', '0.0000000000000000'],
            ['1', '1.0', '+', '2.0000000000000000'],
            ['1', '1.0', '*', '1.0000000000000000'],
            ['0.0', '0', '-', '0.0000000000000000'],
            ['0.0', '0', '+', '0.0000000000000000'],
            ['0.0', '0', '*', '0.0000000000000000'],
            ['1.0', '0', '-', '1.0000000000000000'],
            ['1.0', '0', '+', '1.0000000000000000'],
            ['1.0', '0', '*', '0.0000000000000000'],
            ['1.0', '1', '-', '0.0000000000000000'],
            ['1.0', '1', '+', '2.0000000000000000'],
            ['1.0', '1', '*', '1.0000000000000000'],
            ['1.1', '0', '-', '1.1000000000000000'],
            ['1.1', '0', '+', '1.1000000000000000'],
            ['1.1', '0', '*', '0.0000000000000000'],
            ['1.1', '1', '-', '0.1000000000000000'],
            ['1.1', '1', '+', '2.1000000000000000'],
            ['1.1', '1', '*', '1.1000000000000000'],
            ['0.0', '0.0', '-', '0.0000000000000000'],
            ['0.0', '0.0', '+', '0.0000000000000000'],
            ['0.0', '0.0', '*', '0.0000000000000000'],
            ['1.0', '0.0', '-', '1.0000000000000000'],
            ['1.0', '0.0', '+', '1.0000000000000000'],
            ['1.0', '0.0', '*', '0.0000000000000000'],
            ['1.0', '0.1', '-', '0.9000000000000000'],
            ['1.0', '0.1', '+', '1.1000000000000000'],
            ['1.0', '0.1', '*', '0.1000000000000000'],
            ['1.0', '1.0', '-', '0.0000000000000000'],
            ['1.0', '1.0', '+', '2.0000000000000000'],
            ['1.0', '1.0', '*', '1.0000000000000000'],
            ['1.1', '1.0', '-', '0.1000000000000000'],
            ['1.1', '1.0', '+', '2.1000000000000000'],
            ['1.1', '1.0', '*', '1.1000000000000000'],
            ['1.1', '1.1', '-', '0.0000000000000000'],
            ['1.1', '1.1', '+', '2.2000000000000000'],
            ['1.1', '1.1', '*', '1.2100000000000000'],
            ['18446744073709551609', '1', '+', '18446744073709551610.0000000000000000'],
            ['0.9999999999999998', '0.0000000000000001', '+', '0.9999999999999999'],
            ['0.9999999999999999', '0.0000000000000001', '+', '1.0000000000000000'],
            ['18446744073709551610.9999999999999998', '0.0000000000000001', '+', '18446744073709551610.9999999999999999'],
            ['18446744073709551609.9999999999999998', '1.0000000000000001', '+', '18446744073709551610.9999999999999999'],
            ['18446744073709551609.9999999999999999', '0.0000000000000001', '+', '18446744073709551610.0000000000000000'],
            ['18446744073709551610', '1', '-', '18446744073709551609.0000000000000000'],
            ['0.9999999999999999', '0.0000000000000001', '-', '0.9999999999999998'],
            ['1.0000000000000000', '0.0000000000000001', '-', '0.9999999999999999'],
            ['18446744073709551610.9999999999999999', '1.0000000000000001', '-', '18446744073709551609.9999999999999998'],
            ['18446744073709551610.9999999999999999', '18446744073709551610.9999999999999999', '-', '0.0000000000000000'],
            ['18446744073709551610', '1', '*', '18446744073709551610.0000000000000000'],
            ['9223372036854775805', '2', '*', '18446744073709551610.0000000000000000'],
            ['9223372036854775805.4999999999999999', '2', '*', '18446744073709551610.9999999999999998'],
            ['1277082290674.9475', '14444444.324', '*', '18446744044820663545.3729900000000000'],
            ['14945902123.440573', '1234234234.9999999999999999', '*', '18446744073709551184.6166535054097876']]
            
        #Operators
        operators = ["-", "+", "*"]

        #generate tests
        for i in range(0, generate):
            op_a = Decimal(2.0)
            op_b = Decimal(3.0)
            while op_a - op_b < 0:
                l = 999999999
                op_a_whole = random.randrange(0, l)
                op_a_dec = random.randrange(0, l)
                op_a = Decimal(str(op_a_whole) + "." + str(op_a_dec))
                op_b_whole = random.randrange(0, l)
                op_b_dec = random.randrange(0, l)
                op_b = Decimal(str(op_b_whole) + "." + str(op_b_dec))

            op_a = c.truncate_decimal(str(op_a))
            #op_a = op_a[0:self.precision]
            op_b = c.truncate_decimal(str(op_b))
            #op_b = op_b[0:self.precision]
            for operator in operators:
                whole_no, dec_no = c.math(op_a, op_b, operator, "no")
                test = [op_a, op_b, operator, c.no_to_str(whole_no, dec_no)]
                tests.append(test)


        for test in tests:
            operand_a = test[0]
            operand_b = test[1]
            operator  = test[2]
            expected  = test[3]
            
            if operator == "-":
                actual  = Decimal(operand_a) - Decimal(operand_b)
            if operator == "+":
                actual  = Decimal(operand_a) + Decimal(operand_b)
            if operator == "*":
                actual  = Decimal(operand_a) * Decimal(operand_b)
                
            actual = str(remove_exponent(actual))
            if actual[0] == "-":
                actual = actual[1:]
            expected = str(remove_exponent(Decimal(expected)))
            expected_len = len(expected)
            if expected_len < len(actual):
                actual = actual[:expected_len]

            if expected != actual:
                print(operand_a + " " + operator + " " + operand_b)
                print("We expected: " + str(expected))
                print("But we got : " + str(actual))
                raise Exception("Test currency type failed.")
                assert False
                
        #Test operator overloading.
        assert((C("10.1") == C("10.1")) == True)
        assert((C("10.2") == C("10.1")) == False)
        assert((C("10.1") != C("10.1")) == False)
        assert((C("10.2") != C("10.1")) == True)
        assert((C("10.1") < C("10.1")) == False)
        assert((C("10.1") < C("10.2")) == True)
        assert((C("10.0") <= C("10.1")) == True)
        assert((C("10.1") <= C("10.1")) == True)
        assert((C("10.2") <= C("10.1")) == False)
        assert((C("10.1") > C("10.1")) == False)
        assert((C("10.2") > C("10.1")) == True)
        assert((C("10.0") >= C("10.1")) == False)
        assert((C("10.1") >= C("10.1")) == True)
        assert((C("10.2") >= C("10.1")) == True)
        assert(str(C(str((C("10.2") + C("10.3")) * C("0.2") - C("2.0")))) == "2.1")
        assert(list(C("10.123")) == [10, 1230000000000000])
        assert(len(tuple(C("10.134"))) == 2)
        x = C("10.123")
        x["dec"] = 222
        assert(x == "10.222")
        x["whole"] = 111
        assert(x == "111.222")
