import sqlite3

class Search:

    _connect = sqlite3.connect('sales.sqlite')
    global cursor
    cursor = _connect.cursor()
    maxDiff = None
    
    def department_total(self, dept):
        rows = cursor.execute("SELECT amount FROM sales WHERE department = ?", (dept,)).fetchall()
        sum = 0

        for amount in rows:
            sum += amount[0]
        return sum

    def department_total_bydate(self, dept, date):
        rows = cursor.execute("SELECT amount FROM sales WHERE department = ? AND sale_date = ?", (dept, date),).fetchall()
        sum = 0

        for amount in rows:
            sum += amount[0]
        return sum


    def country_count_date_range(self, country, start_date, end_date):
        buyers = cursor.execute("SELECT id FROM buyers WHERE country = ?", (country,)).fetchall()

        if((start_date[5:7] == "08" and end_date[5:7] == "08") or (start_date[5:7] == "10" and end_date[5:7] == "10")):
            return 0
        elif(start_date[5:7] == "08" and end_date[5:7] == "10"):
            start = 1
            end = 30
        elif(start_date[5:7] == "08"):
            start = 1
            end = int(end_date[8:])
        elif(end_date[5:7] == "10"):
            start = int(start_date[8:])
            end = 30
        else:
            start = int(start_date[8:])
            end = int(end_date[8:])
        sum = 0

        for id in buyers:
            for i in range(start, end + 1):
                if (i < 10):
                    date = "2020-09-0" + str(i)
                else:
                    date = "2020-09-" + str(i)
                buyer = cursor.execute("SELECT amount FROM sales WHERE buyer_id = ? AND sale_date = ?", (int(id[0]), date),).fetchall()
                for amount in buyer:
                    sum += amount[0]
        return sum

    def biggest_spender(self):
        global biggest_id
        biggest = 0
        for i in range(1, 1001):
            buyer = cursor.execute("SELECT amount FROM sales WHERE buyer_id = ?", (i,)).fetchall()
            sum = 0
            for amount in buyer:
                sum += amount[0]
            if (sum > biggest):
                biggest_id = i
                biggest = sum
        return (cursor.execute("SELECT first_name FROM buyers WHERE id = ?", (biggest_id,)).fetchall()[0][0], cursor.execute("SELECT last_name FROM buyers WHERE id = ?", (biggest_id,)).fetchall()[0][0])

    def biggest_spenders(self, how_many, department):
        most_amount_ranked = [] # how_many is how many that should be listed
        most_amount = []
        

        if department == "Not A Department":
            return []
        for i in range(1, 1001):
            sum = 0
            part_amount = cursor.execute("SELECT amount FROM sales WHERE buyer_id = ? AND department = ?", (i, department,)).fetchall()
            print(part_amount)
            for amount in part_amount:
                sum += amount[0]
            most_amount.append((cursor.execute("SELECT first_name FROM buyers WHERE id = ?", (i,)).fetchall()[0][0], cursor.execute("SELECT last_name FROM buyers WHERE id = ?", (i,)).fetchall()[0][0], sum))
        for i in range(how_many):
            biggest = most_amount[0][2]
            for amount in most_amount:
                if amount[2] > biggest:
                    biggest_first_name = amount[0]
                    biggest_last_name = amount[1]
                    biggest = amount[2]
            most_amount_ranked.append(most_amount.pop(most_amount.index((biggest_first_name, biggest_last_name, biggest))))
        return most_amount_ranked
