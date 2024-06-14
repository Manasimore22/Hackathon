from flask import Flask, jsonify ,render_template, jsonify, request,render_template_string
import random
import string
import datetime
from pytz import timezone
import time

app = Flask(__name__)

# Dummy user data
users = [
    # Dummy user data for  Indian people
    {"user_id": 1, "name": "Aarav Patel", "account_number": "11223344556677", "kyc_info": {"id_number": "IN111122", "aadhar_number": "11112222333344", "pan_number": "ABCDE1234A", "address": "45 Gandhi Road, Mumbai", "age": 28, "mobile_number": "9876543201", "annual_income": 75000}},
    {"user_id": 2, "name": "Aanya Singh", "account_number": "22334455667788", "kyc_info": {"id_number": "IN222233", "aadhar_number": "22223333444455", "pan_number": "FGHIJ5678B", "address": "78 Nehru Street, Delhi", "age": 35, "mobile_number": "9876543202", "annual_income": 60000}},
    {"user_id": 3, "name": "Arjun Sharma", "account_number": "33445566778899", "kyc_info": {"id_number": "IN333344", "aadhar_number": "33334444555566", "pan_number": "KLMNO6789C", "address": "12 Vivekananda Nagar, Bangalore", "age": 22, "mobile_number": "9876543203", "annual_income": 70000}},
    {"user_id": 4, "name": "Bhavya Gupta", "account_number": "44556677889900", "kyc_info": {"id_number": "IN444455", "aadhar_number": "44445555666677", "pan_number": "PQRST1234D", "address": "91 Tagore Street, Chennai", "age": 29, "mobile_number": "9876543204", "annual_income": 80000}},
    {"user_id": 5, "name": "Dhruv Verma", "account_number": "55667788990011", "kyc_info": {"id_number": "IN555566", "aadhar_number": "55556666777788", "pan_number": "UVWXY5678E", "address": "34 Ambedkar Avenue, Kolkata", "age": 31, "mobile_number": "9876543205", "annual_income": 90000}},
    {"user_id": 6, "name": "Eva Sharma", "account_number": "66778899001122", "kyc_info": {"id_number": "IN666677", "aadhar_number": "66667777888899", "pan_number": "YZABC6789F", "address": "56 Bose Lane, Pune", "age": 24, "mobile_number": "9876543311", "annual_income": 550000}},
    {"user_id": 7, "name": "Farhan Khan", "account_number": "77889900112233", "kyc_info": {"id_number": "IN777788", "aadhar_number": "77778888999900", "pan_number": "ABCDE1234G", "address": "89 Patel Nagar, Hyderabad", "age": 27, "mobile_number": "9876543312", "annual_income": 600000}},
    {"user_id": 8, "name": "Gia Kapoor", "account_number": "88990011223344", "kyc_info": {"id_number": "IN888899", "aadhar_number": "88889999000011", "pan_number": "FGHIJ5678H", "address": "67 Nehru Street, Bangalore", "age": 33, "mobile_number": "9876543313", "annual_income": 700000}},
    {"user_id": 9, "name": "Hrishikesh Desai", "account_number": "99001122334455", "kyc_info": {"id_number": "IN999900", "aadhar_number": "99990000111122", "pan_number": "KLMNO6789I", "address": "45 Gandhi Road, Ahmedabad", "age": 28, "mobile_number": "9876543314", "annual_income": 800000}},
    {"user_id": 10, "name": "Ishika Mehta", "account_number": "100112233445566", "kyc_info": {"id_number": "IN101112", "aadhar_number": "10111222333444", "pan_number": "PQRST1234J", "address": "78 Nehru Street, Kolkata", "age": 26, "mobile_number": "9876543315", "annual_income": 900000}},
    {"user_id": 11, "name": "Kabir Kapoor", "account_number": "111122233344455", "kyc_info": {"id_number": "IN111223", "aadhar_number": "11122333445566", "pan_number": "ABCDE1234K", "address": "56 Bose Lane, Pune", "age": 24, "mobile_number": "9876543320", "annual_income": 75000}},
    {"user_id": 12, "name": "Leena Desai", "account_number": "122334455566677", "kyc_info": {"id_number": "IN122334", "aadhar_number": "12233444556677", "pan_number": "BCDEF2345L", "address": "89 Patel Nagar, Hyderabad", "age": 27, "mobile_number": "9876543321", "annual_income": 60000}},
    {"user_id": 13, "name": "Manav Verma", "account_number": "133445566677788", "kyc_info": {"id_number": "IN133445", "aadhar_number": "13344555667788", "pan_number": "CDEFG3456M", "address": "67 Nehru Street, Bangalore", "age": 33, "mobile_number": "9876543322", "annual_income": 80000}},
    {"user_id": 14, "name": "Neha Iyer", "account_number": "144556677788899", "kyc_info": {"id_number": "IN144556", "aadhar_number": "14455666778899", "pan_number": "DEFGH4567N", "address": "45 Gandhi Road, Ahmedabad", "age": 28, "mobile_number": "9876543323", "annual_income": 70000}},
    {"user_id": 15, "name": "Ojasvi Reddy", "account_number": "155667788900011", "kyc_info": {"id_number": "IN155667", "aadhar_number": "15566777889900", "pan_number": "EFGHI5678O", "address": "78 Nehru Street, Kolkata", "age": 26, "mobile_number": "9876543324", "annual_income": 90000}},
    {"user_id": 16, "name": "Pranav Thakur", "account_number": "166778899001122", "kyc_info": {"id_number": "IN166778", "aadhar_number": "16677888990011", "pan_number": "FGHIJ6789P", "address": "34 Ambedkar Avenue, Chennai", "age": 31, "mobile_number": "9876543325", "annual_income": 75000}},
    {"user_id": 17, "name": "Qureshi Khan", "account_number": "177889900112233", "kyc_info": {"id_number": "IN177889", "aadhar_number": "17788999001122", "pan_number": "GHIJK7890Q", "address": "12 Vivekananda Nagar, Mumbai", "age": 29, "mobile_number": "9876543326", "annual_income": 100000}},
    {"user_id": 18, "name": "Ritika Sharma", "account_number": "188900112233445", "kyc_info": {"id_number": "IN188900", "aadhar_number": None, "pan_number": "HIJKL8901R", "address": "91 Tagore Street, Delhi", "age": 22, "mobile_number": "9876543313", "annual_income": 80000}},
    {"user_id": 19, "name": "Sahil Gupta", "account_number": "199011223344556", "kyc_info": {"id_number": "IN199011", "aadhar_number": "19901111223344", "pan_number": "IJKLM9012S", "address": "45 Gandhi Road, Kolkata", "age": 29, "mobile_number": "9876543328", "annual_income": 95000}},
    {"user_id": 20, "name": "Tanvi Singh", "account_number": "200112233445566", "kyc_info": {"id_number": "IN200112", "aadhar_number": "20011222334455", "pan_number": "JKLMN0123T", "address": "34 Ambedkar Avenue, Pune", "age": 31, "mobile_number": "9876543329", "annual_income": 85000}},
    {"user_id": 21, "name": "Uday Singh", "account_number": "211223344455566", "kyc_info": {"id_number": "IN211223", "aadhar_number": "21122333445566", "pan_number": "ABCDE1234U", "address": "56 Bose Lane, Pune", "age": 24, "mobile_number": "9876543330", "annual_income": 200000}},
    {"user_id": 22, "name": "Varsha Patel", "account_number": "222334455566677", "kyc_info": {"id_number": "IN222334", "aadhar_number": "22233444556677", "pan_number": "FGHIJ5678V", "address": "89 Patel Nagar, Hyderabad", "age": 27, "mobile_number": "9876543331", "annual_income": 60000}},
    {"user_id": 23, "name": "Waqar Khan", "account_number": "233445556667788", "kyc_info": {"id_number": "IN233445", "aadhar_number": "23344555667788", "pan_number": "KLMNO6789W", "address": "67 Nehru Street, Bangalore", "age": 33, "mobile_number": "9876543332", "annual_income": 300000}},
    {"user_id": 24, "name": "Xena Gupta", "account_number": "244556667788899", "kyc_info": {"id_number": "IN244556", "aadhar_number": "24455666778899", "pan_number": "PQRST1234X", "address": "45 Gandhi Road, Ahmedabad", "age": 28, "mobile_number": "9876543333", "annual_income": 70000}},
    {"user_id": 25, "name": "Yuvan Verma", "account_number": "255667778889900", "kyc_info": {"id_number": "IN255667", "aadhar_number": "25566777889900", "pan_number": "UVWXY5678Y", "address": "78 Nehru Street, Kolkata", "age": 26, "mobile_number": "9876543334", "annual_income": 90000}},
    {"user_id": 26, "name": "Zara Khan", "account_number": "26667778889900", "kyc_info": {"id_number": "IN266677", "aadhar_number": "26667778889900", "pan_number": "UVWXY5678Z", "address": "34 Gandhi Road, Mumbai", "age": 32, "mobile_number": "9876543335", "annual_income": 85000}},
    {"user_id": 27, "name": "Rohan Sharma", "account_number": "277788899001122", "kyc_info": {"id_number": "IN277788", "aadhar_number": "27778889900122", "pan_number": "ABCDE1234L", "address": "56 Nehru Street, Delhi", "age": 25, "mobile_number": "9876543336", "annual_income": 300000}},
    {"user_id": 28, "name": "Priya Kapoor", "account_number": "288899900112233", "kyc_info": {"id_number": "IN288899", "aadhar_number": "288899900112233", "pan_number": "FGHIJ5678M", "address": "78 Tagore Street, Bangalore", "age": 30, "mobile_number": "9876543337", "annual_income": 700000}},
    {"user_id": 29, "name": "Shaan Verma", "account_number": "299900011223344", "kyc_info": {"id_number": "IN299900", "aadhar_number": None, "pan_number": "KLMNO6789N", "address": "12 Vivekananda Nagar, Chennai", "age": 28, "mobile_number": "9876543313", "annual_income": 78000}},
    {"user_id": 30, "name": "Ishita Gupta", "account_number": "300011223344556", "kyc_info": {"id_number": "IN300011", "aadhar_number": "300011223344556", "pan_number": "PQRST1234O", "address": None, "age": 34, "mobile_number": "9876543213", "annual_income": 650000}},
    {"user_id": 31, "name": "Rajeev Desai", "account_number": "311122334455667", "kyc_info": {"id_number": "IN311122", "aadhar_number": "311122334455667", "pan_number": "ABCDE1234P", "address": "45 Bose Lane, Pune", "age": 29, "mobile_number": "9876543340", "annual_income": 400000}},
    {"user_id": 32, "name": "Tanish Singh", "account_number": "322233344455566", "kyc_info": {"id_number": "IN322233", "aadhar_number": "322233344455566", "pan_number": "FGHIJ5678B", "address": "56 Patel Nagar, Hyderabad", "age": 31, "mobile_number": "9876543313", "annual_income": 150000}},
    {"user_id": 33, "name": "Vidya Sharma", "account_number": "333344455566677", "kyc_info": {"id_number": "IN333344", "aadhar_number": "333344455566677", "pan_number": "KLMNO6789R", "address": "89 Nehru Street, Ahmedabad", "age": 27, "mobile_number": "9876543342", "annual_income": 80000}},
    {"user_id": 34, "name": "Akshay Patel", "account_number": "344455566677788", "kyc_info": {"id_number": "IN344455", "aadhar_number": "344455566677788", "pan_number": "PQRST1234S", "address": "67 Gandhi Road, Mumbai", "age": 26, "mobile_number": "9876543343", "annual_income": 75000}},
    {"user_id": 35, "name": "Ananya Verma", "account_number": "355566677788899", "kyc_info": {"id_number": "IN355566", "aadhar_number": "355566677788899", "pan_number": "UVWXY5678T", "address": "78 Nehru Street, Delhi", "age": 24, "mobile_number": "9876543344", "annual_income": 65000}},
    {"user_id": 36, "name": "Rishi Thakur", "account_number": "366677788899900", "kyc_info": {"id_number": "IN366677", "aadhar_number": "366677788899900", "pan_number": "ABCDE1234U", "address": "34 Vivekananda Nagar, Bangalore", "age": 35, "mobile_number": "9876543345", "annual_income": 70000}},
    {"user_id": 37, "name": "Ishaan Khan", "account_number": "377788899001122", "kyc_info": {"id_number": "IN377788", "aadhar_number": None, "pan_number": "FGHIJ5678V", "address": "56 Tagore Street, Chennai", "age": 29, "mobile_number": "9876543344", "annual_income": 95000}},
    {"user_id": 38, "name": "Trisha Sharma", "account_number": "388899900112233", "kyc_info": {"id_number": "IN388899", "aadhar_number": "388899900112233", "pan_number": "KLMNO6789W", "address": "91 Ambedkar Avenue, Kolkata", "age": 28, "mobile_number": "9876543347", "annual_income": 120000}},
    {"user_id": 39, "name": "Aarush Gupta", "account_number": "399900011223344", "kyc_info": {"id_number": "IN399900", "aadhar_number": "399900011223344", "pan_number": "PQRST1234X", "address": "12 Bose Lane, Pune", "age": 34, "mobile_number": "9876543348", "annual_income": 200000}},
    {"user_id": 40, "name": "Aisha Singh", "account_number": "400011223344556", "kyc_info": {"id_number": "IN400011", "aadhar_number": "400011223344556", "pan_number": "ABCDE1234Y", "address": "56 Patel Nagar, Hyderabad", "age": 31, "mobile_number": "9876543349", "annual_income": 300000}},
    {"user_id": 41, "name": "Rudra Kapoor", "account_number": "411122334455667", "kyc_info": {"id_number": "IN411122", "aadhar_number": "411122334455667", "pan_number": "FGHIJ5678Z", "address": "67 Nehru Street, Ahmedabad", "age": 27, "mobile_number": "9876543350", "annual_income": 80000}},
    {"user_id": 42, "name": "Arya Sharma", "account_number": "422233344455566", "kyc_info": {"id_number": "IN422233", "aadhar_number": "422233344455566", "pan_number": "KLMNO6789A", "address": "89 Gandhi Road, Mumbai", "age": 26, "mobile_number": "9876543351", "annual_income": 120000}},
    {"user_id": 43, "name": "Veer Verma", "account_number": "433344455566677", "kyc_info": {"id_number": "IN433344", "aadhar_number": None, "pan_number": "PQRST1234B", "address": "34 Nehru Street, Delhi", "age": 24, "mobile_number": "9876543344", "annual_income": 180000}},
    {"user_id": 44, "name": "Aradhya Patel", "account_number": "444455566677788", "kyc_info": {"id_number": "IN444455", "aadhar_number": "444455566677788", "pan_number": "UVWXY5678C", "address": "56 Tagore Street, Bangalore", "age": 35, "mobile_number": "9876543353", "annual_income": 300000}},
    {"user_id": 45, "name": "Vihaan Khan", "account_number": "455566677788899", "kyc_info": {"id_number": "IN455566", "aadhar_number": "455566677788899", "pan_number": "ABCDE1234D", "address": "78 Ambedkar Avenue, Kolkata", "age": 29, "mobile_number": "9876543354", "annual_income": 200000}},
    {"user_id": 46, "name": "Anvi Verma", "account_number": "466677788899900", "kyc_info": {"id_number": "IN466677", "aadhar_number": "466677788899900", "pan_number": "FGHIJ5678E", "address": "12 Vivekananda Nagar, Chennai", "age": 28, "mobile_number": "9876543355", "annual_income": 180000}},
    {"user_id": 47, "name": "Reyansh Sharma", "account_number": "477788899001122", "kyc_info": {"id_number": "IN477788", "aadhar_number": "477788899001122", "pan_number": "KLMNO6789F", "address": "45 Bose Lane, Pune", "age": 34, "mobile_number": "9876543356", "annual_income": 150000}},
    {"user_id": 48, "name": "Aarna Singh", "account_number": "488899900112233", "kyc_info": {"id_number": "IN488899", "aadhar_number": "488899900112233", "pan_number": "PQRST1234G", "address": "56 Patel Nagar, Hyderabad", "age": 31, "mobile_number": "9876543357", "annual_income": 120000}},
    {"user_id": 49, "name": "Arjun Thakur", "account_number": "499900011223344", "kyc_info": {"id_number": "IN499900", "aadhar_number": "499900011223344", "pan_number": "ABCDE1234H", "address": "67 Ambedkar Avenue, Mumbai", "age": 29, "mobile_number": "9876543358", "annual_income": 40000}},
    {"user_id": 50, "name": "Aaradhya Gupta", "account_number": "500011223344556", "kyc_info": {"id_number": "IN500011", "aadhar_number": "500011223344556", "pan_number": "FGHIJ5678I", "address": "89 Tagore Street, Delhi", "age": 32, "mobile_number": "9876543359", "annual_income": 2800000}},
    {"user_id": 51, "name": "Zayn Kapoor", "account_number": "511122334455667", "kyc_info": {"id_number": "IN511122", "aadhar_number": "511122334455667", "pan_number": "FGHIJ5678A", "address": "67 Nehru Street, Ahmedabad", "age": 27, "mobile_number": "9876543360", "annual_income": 150000}},
    {"user_id": 52, "name": "Anvi Sharma", "account_number": "522233344455566", "kyc_info": {"id_number": "IN522233", "aadhar_number": None, "pan_number": "KLMNO6789B", "address": "89 Gandhi Road, Mumbai", "age": 26, "mobile_number": "9876543344", "annual_income": 120000}},
    {"user_id": 53, "name": "Vihan Verma", "account_number": "533344455566677", "kyc_info": {"id_number": "IN533344", "aadhar_number": "533344455566677", "pan_number": "PQRST1234C", "address": None, "age": 24, "mobile_number": "9876543362", "annual_income": 90000}},
    {"user_id": 54, "name": "Aranya Patel", "account_number": "544455566677788", "kyc_info": {"id_number": "IN544455", "aadhar_number": "544455566677788", "pan_number": "UVWXY5678D", "address": "56 Tagore Street, Bangalore", "age": 35, "mobile_number": "9876543363", "annual_income": 70000}},
    {"user_id": 55, "name": "Vivaan Khan", "account_number": "555566677788899", "kyc_info": {"id_number": "IN555566", "aadhar_number": "555566677788899", "pan_number": "ABCDE1234E", "address": "78 Ambedkar Avenue, Kolkata", "age": 29, "mobile_number": "9876543364", "annual_income": 80000}},
    {"user_id": 56, "name": "Anika Verma", "account_number": "566677788899900", "kyc_info": {"id_number": "IN566677", "aadhar_number": "566677788899900", "pan_number": "FGHIJ5678F", "address": "12 Vivekananda Nagar, Chennai", "age": 28, "mobile_number": "9876543365", "annual_income": 78000}},
    {"user_id": 57, "name": "Rehan Sharma", "account_number": "577788899001122", "kyc_info": {"id_number": "IN577788", "aadhar_number": "577788899001122", "pan_number": "KLMNO6789G", "address": "45 Bose Lane, Pune", "age": 34, "mobile_number": "9876543366", "annual_income": 60000}},
    {"user_id": 58, "name": "Aadhya Singh", "account_number": "588899900112233", "kyc_info": {"id_number": "IN588899", "aadhar_number": "588899900112233", "pan_number": "PQRST1234H", "address": "56 Patel Nagar, Hyderabad", "age": 31, "mobile_number": "9876543367", "annual_income": 90000}},
    {"user_id": 59, "name": "Arnav Thakur", "account_number": "599900011223344", "kyc_info": {"id_number": "IN599900", "aadhar_number": "599900011223344", "pan_number": "ABCDE1234I", "address": "67 Ambedkar Avenue, Mumbai", "age": 29, "mobile_number": "9876543368", "annual_income": 85000}},
    {"user_id": 60, "name": "Aanya Gupta", "account_number": "600011223344556", "kyc_info": {"id_number": "IN600011", "aadhar_number": "600011223344556", "pan_number": "FGHIJ5678J", "address": "89 Tagore Street, Delhi", "age": 32, "mobile_number": "9876543369", "annual_income": 120000}},
    {"user_id": 61, "name": "Rohan Verma", "account_number": "611122334455667", "kyc_info": {"id_number": "IN611122", "aadhar_number": None, "pan_number": "KLMNO6789K", "address": "67 Nehru Street, Ahmedabad", "age": 27, "mobile_number": "9876543363", "annual_income": 150000}},
    {"user_id": 62, "name": "Aarav Sharma", "account_number": "622233344455566", "kyc_info": {"id_number": "IN622233", "aadhar_number": "622233344455566", "pan_number": "PQRST1234L", "address": "89 Gandhi Road, Mumbai", "age": 26, "mobile_number": "9876543371", "annual_income": 120000}},
    {"user_id": 63, "name": "Zara Verma", "account_number": "633344455566677", "kyc_info": {"id_number": "IN633344", "aadhar_number": "633344455566677", "pan_number": "UVWXY5678M", "address": "34 Nehru Street, Delhi", "age": 24, "mobile_number": "9876543372", "annual_income": 90000}},
    {"user_id": 64, "name": "Vihaan Patel", "account_number": "644455566677788", "kyc_info": {"id_number": "IN644455", "aadhar_number": "644455566677788", "pan_number": "ABCDE1234S", "address": "56 Tagore Street, Bangalore", "age": 35, "mobile_number": "9876543373", "annual_income": 70000}},
    {"user_id": 65, "name": "Aria Khan", "account_number": "655566677788899", "kyc_info": {"id_number": "IN655566", "aadhar_number": "655566677788899", "pan_number": "ABCDE1234N", "address": "78 Ambedkar Avenue, Kolkata", "age": 29, "mobile_number": "9876543374", "annual_income": 80000}},
    {"user_id": 66, "name": "Anirudh Verma", "account_number": "666677788899900", "kyc_info": {"id_number": "IN666677", "aadhar_number": "666677788899900", "pan_number": "FGHIJ5678O", "address": "12 Vivekananda Nagar, Chennai", "age": 28, "mobile_number": "9876543375", "annual_income": 78000}},
    {"user_id": 67, "name": "Aisha Sharma", "account_number": "677788899001122", "kyc_info": {"id_number": "IN677788", "aadhar_number": "677788899001122", "pan_number": "KLMNO6789P", "address": "45 Bose Lane, Pune", "age": 34, "mobile_number": "9876543376", "annual_income": 60000}},
    {"user_id": 68, "name": "Aarav Singh", "account_number": "688899900112233", "kyc_info": {"id_number": "IN688899", "aadhar_number": "688899900112233", "pan_number": "PQRST1234Q", "address": "56 Patel Nagar, Hyderabad", "age": 31, "mobile_number": "9876543377", "annual_income": 90000}},
    {"user_id": 69, "name": "Aradhya Thakur", "account_number": "699900011223344", "kyc_info": {"id_number": "IN699900", "aadhar_number": "699900011223344", "pan_number": "ABCDE1234R", "address": "67 Ambedkar Avenue, Mumbai", "age": 29, "mobile_number": "9876543378", "annual_income": 85000}},
    {"user_id": 70, "name": "Aarush Gupta", "account_number": "700011223344556", "kyc_info": {"id_number": "IN700011", "aadhar_number": None, "pan_number": "FGHIJ5678S", "address": "89 Tagore Street, Delhi", "age": 32, "mobile_number": "9876543363", "annual_income": 120000}},
    {"user_id": 71, "name": "Anvi Verma", "account_number": "711122334455667", "kyc_info": {"id_number": "IN711122", "aadhar_number": "711122334455667", "pan_number": "KLMNO6789T", "address": "67 Nehru Street, Ahmedabad", "age": 27, "mobile_number": "9876543380", "annual_income": 150000}},
    {"user_id": 72, "name": "Zayan Sharma", "account_number": "722233344455566", "kyc_info": {"id_number": "IN722233", "aadhar_number": "722233344455566", "pan_number": "PQRST1234U", "address": "89 Gandhi Road, Mumbai", "age": 26, "mobile_number": "9876543381", "annual_income": 120000}},
    {"user_id": 73, "name": "Aaradhya Patel", "account_number": "733344455566677", "kyc_info": {"id_number": "IN733344", "aadhar_number": "733344455566677", "pan_number": "UVWXY5678V", "address": "34 Nehru Street, Delhi", "age": 24, "mobile_number": "9876543382", "annual_income": 90000}},
    {"user_id": 74, "name": "Aarav Thakur", "account_number": "744455566677788", "kyc_info": {"id_number": "IN744455", "aadhar_number": "744455566677788", "pan_number": "ABCDE1234W", "address": "56 Tagore Street, Bangalore", "age": 35, "mobile_number": "9876543383", "annual_income": 70000}},
    {"user_id": 75, "name": "Anaya Khan", "account_number": "755566677788899", "kyc_info": {"id_number": "IN755566", "aadhar_number": "755566677788899", "pan_number": "PQRST1234X", "address": "78 Ambedkar Avenue, Kolkata", "age": 29, "mobile_number": "9876543384", "annual_income": 80000}},
    {"user_id": 76, "name": "Zara Kapoor", "account_number": "766677788899900", "kyc_info": {"id_number": "IN766677", "aadhar_number": "766677788899900", "pan_number": "FGHIJ5678Z", "address": "12 Vivekananda Nagar, Pune", "age": 28, "mobile_number": "9876543385", "annual_income": 78000}},
    {"user_id": 77, "name": "Arjun Sharma", "account_number": "778899001122233", "kyc_info": {"id_number": "IN778899", "aadhar_number": "778899001122233", "pan_number": "KLMNO6789A", "address": "45 Bose Lane, Chennai", "age": 34, "mobile_number": "9876543386", "annual_income": 60000}},
    {"user_id": 78, "name": "Aaradhya Singh", "account_number": "789900011223344", "kyc_info": {"id_number": "IN789900", "aadhar_number": "789900011223344", "pan_number": "PQRST1234B", "address": "56 Patel Nagar, Hyderabad", "age": 31, "mobile_number": "9876543387", "annual_income": 90000}},
    {"user_id": 79, "name": "Aadit Thakur", "account_number": "790011223344556", "kyc_info": {"id_number": "IN790011", "aadhar_number": "790011223344556", "pan_number": "FGHIJ5678C", "address": "89 Tagore Street, Delhi", "age": 32, "mobile_number": "9876543388", "annual_income": 85000}},
    {"user_id": 80, "name": "Anika Gupta", "account_number": "801122334455667", "kyc_info": {"id_number": "IN801122", "aadhar_number": "801122334455667", "pan_number": "UVWXY5678D", "address": "67 Nehru Street, Mumbai", "age": 27, "mobile_number": "9876543389", "annual_income": 80000}},
    {"user_id": 81, "name": "Vihaan Verma", "account_number": "812233344455566", "kyc_info": {"id_number": "IN812233", "aadhar_number": None, "pan_number": "ABCDE1234E", "address": "78 Ambedkar Avenue, Kolkata", "age": 29, "mobile_number": "9876543363", "annual_income": 90000}},
    {"user_id": 82, "name": "Aarush Patel", "account_number": "823344455566677", "kyc_info": {"id_number": "IN823344", "aadhar_number": "823344455566677", "pan_number": "FGHIJ5678F", "address": "56 Tagore Street, Bangalore", "age": 35, "mobile_number": "9876543391", "annual_income": 70000}},
    {"user_id": 83, "name": "Anvi Khan", "account_number": "834455566677788", "kyc_info": {"id_number": "IN834455", "aadhar_number": "834455566677788", "pan_number": "PQRST1234G", "address": "45 Gandhi Road, Pune", "age": 28, "mobile_number": "9876543392", "annual_income": 78000}},
    {"user_id": 84, "name": "Zayan Thakur", "account_number": "845566677788899", "kyc_info": {"id_number": "IN845566", "aadhar_number": "845566677788899", "pan_number": "UVWXY5678H", "address": "34 Nehru Street, Ahmedabad", "age": 24, "mobile_number": "9876543393", "annual_income": 65000}},
    {"user_id": 85, "name": "Aria Verma", "account_number": "856677788899900", "kyc_info": {"id_number": "IN856677", "aadhar_number": "856677788899900", "pan_number": "ABCDE1234I", "address": "12 Vivekananda Nagar, Mumbai", "age": 33, "mobile_number": "9876543394", "annual_income": 95000}},
    {"user_id": 86, "name": "Aayush Sharma", "account_number": "867788899001122", "kyc_info": {"id_number": "IN867788", "aadhar_number": "867788899001122", "pan_number": "FGHIJ5678J", "address": "56 Patel Nagar, Delhi", "age": 31, "mobile_number": "9876543395", "annual_income": 85000}},
    {"user_id": 87, "name": "Anvi Singh", "account_number": "878899900112233", "kyc_info": {"id_number": "IN878899", "aadhar_number": "878899900112233", "pan_number": "PQRST1234K", "address": "89 Tagore Street, Hyderabad", "age": 29, "mobile_number": "9876543396", "annual_income": 80000}},
    {"user_id": 88, "name": "Ziva Thakur", "account_number": "889900011223344", "kyc_info": {"id_number": "IN889900", "aadhar_number": "889900011223344", "pan_number": "ABCDE1234L", "address": "67 Ambedkar Avenue, Kolkata", "age": 32, "mobile_number": "9876543397", "annual_income": 75000}},
    {"user_id": 89, "name": "Aarav Gupta", "account_number": "900011223344556", "kyc_info": {"id_number": "IN900011", "aadhar_number": "900011223344556", "pan_number": "FGHIJ5678M", "address": "56 Patel Nagar, Pune", "age": 27, "mobile_number": "9876543398", "annual_income": 70000}},
    {"user_id": 90, "name": "Aradhya Verma", "account_number": "911122334455667", "kyc_info": {"id_number": "IN911122", "aadhar_number": None, "pan_number": "UVWXY5678N", "address": "78 Ambedkar Avenue, Bangalore", "age": 26, "mobile_number": "9876543397", "annual_income": 60000}},
    {"user_id": 91, "name": "Aanya Patel", "account_number": "922233344455566", "kyc_info": {"id_number": "IN922233", "aadhar_number": "922233344455566", "pan_number": "ABCDE1234O", "address": "45 Bose Lane, Chennai", "age": 28, "mobile_number": "9876543400", "annual_income": 78000}},
    {"user_id": 92, "name": "Aarav Khan", "account_number": "933344455566677", "kyc_info": {"id_number": "IN933344", "aadhar_number": "933344455566677", "pan_number": "PQRST1234P", "address": "56 Tagore Street, Pune", "age": 35, "mobile_number": "9876543401", "annual_income": 90000}},
    {"user_id": 93, "name": "Anaya Thakur", "account_number": "944455566677788", "kyc_info": {"id_number": "IN944455", "aadhar_number": None, "pan_number": "FGHIJ5678Q", "address": "89 Patel Nagar, Ahmedabad", "age": 24, "mobile_number": "9876543497", "annual_income": 85000}},
    {"user_id": 94, "name": "Aarush Singh", "account_number": "955566677788899", "kyc_info": {"id_number": "IN955566", "aadhar_number": "955566677788899", "pan_number": "UVWXY5678R", "address": "67 Nehru Street, Delhi", "age": 29, "mobile_number": "9876543403", "annual_income": 80000}},
    {"user_id": 95, "name": "Aaradhya Sharma", "account_number": "966677788899900", "kyc_info": {"id_number": "IN966677", "aadhar_number": "966677788899900", "pan_number": "ABCDE1234S", "address": "45 Bose Lane, Hyderabad", "age": 31, "mobile_number": "9876543404", "annual_income": 70000}},
    {"user_id": 96, "name": "Zayn Khan", "account_number": "977788899001122", "kyc_info": {"id_number": "IN977788", "aadhar_number": "977788899001122", "pan_number": "PQRST1234T", "address": "56 Patel Nagar, Bangalore", "age": 32, "mobile_number": "9876543405", "annual_income": 78000}},
    {"user_id": 97, "name": "Anvi Thakur", "account_number": "988899900112233", "kyc_info": {"id_number": "IN988899", "aadhar_number": "988899900112233", "pan_number": "UVWXY5678U", "address": "89 Tagore Street, Mumbai", "age": 27, "mobile_number": "9876543406", "annual_income": 90000}},
    {"user_id": 98, "name": "Aayan Verma", "account_number": "999900011223344", "kyc_info": {"id_number": "IN999900", "aadhar_number": "999900011223344", "pan_number": "ABCDE1234V", "address": "67 Ambedkar Avenue, Kolkata", "age": 33, "mobile_number": "9876543407", "annual_income": 95000}},
    {"user_id": 99, "name": "Aarav Singh", "account_number": "100011223344556", "kyc_info": {"id_number": "IN100011", "aadhar_number": "100011223344556", "pan_number": "FGHIJ5678W", "address": "56 Patel Nagar, Pune", "age": 28, "mobile_number": "9876543408", "annual_income": 80000}},
    {"user_id": 100, "name": "Aadhya Kapoor", "account_number": "101122334455667", "kyc_info": {"id_number": "IN101122", "aadhar_number": "101122334455667", "pan_number": "PQRST1234X", "address": "78 Ambedkar Avenue, Bangalore", "age": 29, "mobile_number": "9876543409", "annual_income": 75000}}

        ]

# Generate a random transaction ID
def generate_transaction_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Dummy endpoint to simulate transactions
@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if request.method == 'POST':
        # Set Indian time zone (IST)
        
        ist = timezone('Asia/Kolkata')

        # Get the start time
        start_time = datetime.datetime.now(ist)

        # Select a random sender
        sender = random.choice(users)

        # Set the same amount to be debited from the sender's account
        amount_to_debit = round(random.uniform(10.0, 10000.0), 2)

        # Select a random recipient different from the sender
        recipient = random.choice([u for u in users if u != sender])

        # Get a random timestamp within a one-minute window
        timestamp_str = (start_time + datetime.timedelta(seconds=random.randint(0, 59))).strftime('%Y-%m-%dT%H:%M:%S')

        # Create the transaction
        transaction = {
            "transaction_id": generate_transaction_id(),
            "sender_name": sender["name"],
            "sender_account_number": sender["account_number"],
            "sender_kyc_info": sender["kyc_info"],
            "recipient_name": recipient["name"],
            "recipient_account_number": recipient["account_number"],
            "recipient_kyc_info": recipient["kyc_info"],
            "amount": amount_to_debit,
            "timestamp": timestamp_str,
            "place": f"{random.choice(['ATM', 'Online', 'Store'])} {random.randint(1, 10)}",
            "type": "Debit"
        }
        
        return jsonify(transaction)

    elif request.method == 'GET':
        return render_template_string("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Transactions</title>
                <style>
                    table {
                        font-family: Arial, sans-serif;
                        border-collapse: collapse;
                        width: 100%;
                    }
                    th, td {
                        border: 1px solid #dddddd;
                        text-align: left;
                        padding: 8px;
                    }
                    tr:nth-child(even) {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <h1>Transactions</h1>
                <table id="transactions-table">
                    <tr>
                        <th>Transaction ID</th>
                        <th>Sender</th>
                        <th>Sender Account Number</th>
                        <th>Sender KYC Info</th>
                        <th>Recipient</th>
                        <th>Recipient Account Number</th>
                        <th>Recipient KYC Info</th>
                        <th>Amount</th>
                        <th>Timestamp</th>
                        <th>Place</th>
                        <th>Type</th>
                    </tr>
                </table>

                <script>
                    function fetchNewTransaction() {
                        fetch('/transactions', { method: 'POST' })
                        .then(response => response.json())
                        .then(transaction => {
                            const table = document.getElementById('transactions-table');
                            const row = table.insertRow(1);
                            row.innerHTML = `
                                <td>${transaction.transaction_id}</td>
                                <td>${transaction.sender_name}</td>
                                <td>${transaction.sender_account_number}</td>
                                <td>${transaction.sender_kyc_info.address}</td>
                                <td>${transaction.recipient_name}</td>
                                <td>${transaction.recipient_account_number}</td>
                                <td>${transaction.recipient_kyc_info.address}</td>
                                <td>${transaction.amount}</td>
                                <td>${transaction.timestamp}</td>
                                <td>${transaction.place}</td>
                                <td>${transaction.type}</td>
                            `;
                        });
                    }

                    // Fetch new transaction every 1 seconds
                    setInterval(fetchNewTransaction, 1000);
                </script>
            </body>
            </html>
            """)

if __name__ == '__main__':
    app.run(debug=True)
    