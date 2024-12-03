import sys

import mysql.connector
import mysql.connector.abstracts
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from collections import namedtuple

# from enter_new_batch import *
# from spray_print_menu import *

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="UL1131",
    database="production_dupe"
)

# mydb = mysql.connector.connect(
#     host="192.168.1.17",
#     user="admin",
#     password="UL1131",
#     database="production"
# )

my_cursor = mydb.cursor()

class ExtendedComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)


    # on selection of an item from the completer, select the corresponding item from combobox 
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))


    # on model change, update the models of the filter and completer as well 
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)


    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)    

class main_menu(QWidget):
   def __init__(self, parent = None):
      super(main_menu,self).__init__(parent)

      my_cursor.execute("SELECT part_name, part_code FROM main_parts")
      all_parts_info = my_cursor.fetchall()
      parts_tuple = namedtuple("parts_info", ["part_name", "part_code"])
      #part will become part in all_parts, then inputs into parts_info for namedtuple * to unzip the tuple that is pass through 
      parts = [parts_tuple(*part) for part in all_parts_info]
      self.part_codes = [part.part_code for part in parts]  
      self.part_name = [part.part_name for part in parts]

      layout = QHBoxLayout()
      self.resize(200,50)
      self.setWindowTitle("Main Menu")

      self.b1 = QPushButton("New Batch")
      self.b1.setCheckable(True)
      self.b1.clicked.connect(self.open_spray_print_window)
      layout.addWidget(self.b1)

      self.b2 = QPushButton("100 % Spray")
      self.b2.setCheckable(True)
      self.b2.clicked.connect(self.open_first_phase_checking_window)
      layout.addWidget(self.b2)

      self.b3 = QPushButton("100 % Print")
      self.b3.setCheckable(True)
      self.b3.clicked.connect(self.open_first_phase_print_checking_window)
      layout.addWidget(self.b3)

      self.b4 = QPushButton("200 %")
      self.b4.setCheckable(True)
      self.b4.clicked.connect(self.open_finished_goods_checking_window)
      layout.addWidget(self.b4)

      self.b4 = QPushButton("To Store")
      self.b4.setCheckable(True)
      self.b4.clicked.connect(self.open_to_store_window)
      layout.addWidget(self.b4)

      self.b5 = QPushButton("Rework")
      self.b5.setCheckable(True)
      self.b5.clicked.connect(self.open_rework_window)
      layout.addWidget(self.b5)

      self.setLayout(layout)

      self.spray_print_window = None
      self.first_phase_window = None
      self.finished_goods_checking_window = None
      self.to_store_window = None
      self.rework_window = None
      self.first_phase_print_window = None
   
   def open_spray_print_window(self):
        # Check if the spray_print window is already open; if not, create it
        if self.spray_print_window is None:
            self.spray_print_window = spray_print_window(self.part_codes)
        
        # Show the spray_print window
        self.spray_print_window.show()

   def open_first_phase_checking_window(self):
        # Check if the spray_print window is already open; if not, create it
        if self.first_phase_window is None:
            self.first_phase_window = first_phase_checking()
        
        # Show the spray_print window
        self.first_phase_window.show()

   def open_first_phase_print_checking_window(self):
        # Check if the spray_print window is already open; if not, create it
        if self.first_phase_print_window is None:
            self.first_phase_print_window = first_phase_checking_print()
        
        # Show the spray_print window
        self.first_phase_print_window.show()
 
   def open_finished_goods_checking_window(self):
        # Check if the spray_print window is already open; if not, create it
        if self.finished_goods_checking_window is None:
            self.finished_goods_checking_window = finished_goods_checking()
        
        # Show the spray_print window
        self.finished_goods_checking_window.show()

   def open_to_store_window(self):
        # Check if the spray_print window is already open; if not, create it
        if self.to_store_window is None:
            self.to_store_window = to_store()
        
        # Show the spray_print window
        self.to_store_window.show()

   def open_rework_window(self):
        # Check if the spray_print window is already open; if not, create it
        if self.rework_window is None:
            self.rework_window = rework_checking()
        
        # Show the spray_print window
        self.rework_window.show()


class spray_print_window(QWidget):
   def __init__(self, part_codes, parent = None):
      super(spray_print_window,self).__init__(parent)
      self.part_codes = part_codes

      layout = QHBoxLayout()
      self.resize(200,50)
      self.setWindowTitle("Menu")

      self.b1 = QPushButton("Spray")
      self.b1.setCheckable(True)
      self.b1.clicked.connect(self.open_new_batch_spray_entry_window)
      layout.addWidget(self.b1)

      self.b2 = QPushButton("Print")
      self.b2.setCheckable(True)
      self.b2.clicked.connect(self.open_print_batch_entry)
      layout.addWidget(self.b2)

      self.setLayout(layout)

      self.new_batch_spray_entry_window = None
      self.open_new_batch_print_window = None

   def open_new_batch_spray_entry_window(self):
        # Check if the spray_print window is already open; if not, create it
        if self.new_batch_spray_entry_window is None:
            self.new_batch_spray_entry_window = new_batch_spray_entry_window(self.part_codes)
        
        # Show the new_batch_spray_entry_window window
        self.new_batch_spray_entry_window.show()

   def open_print_batch_entry(self):
       # Check if the new_print_batch_entry_window window is already open; if not, create it
        if self.open_new_batch_print_window is None:
            self.open_new_batch_print_window = open_new_batch_print_window(self.part_codes)
        
        # Show the open_new_batch_print_window window
        self.open_new_batch_print_window.show()

class new_batch_spray_entry_window(QWidget):
   def __init__(self, part_codes, parent = None):
      super(new_batch_spray_entry_window,self).__init__(parent)

      self.setWindowTitle("Enter New Spray Batch")
      layout = QVBoxLayout()

      self.part_code_entry = ExtendedComboBox()
      self.part_code_entry.addItems(part_codes)
      layout.addWidget(self.part_code_entry)
      # Product code
    #   self.part_code_entry = QComboBox()
    #   self.part_code_entry.addItems(part_codes)
    #   layout.addWidget(self.part_code_entry)

      #Output amount
      self.e1 = QLineEdit()
      self.e1.setValidator(QIntValidator())
      self.e1.setMaxLength(4)
      self.e1.setAlignment(Qt.AlignRight)

      #Reject amount
      self.e2 = QLineEdit()
      self.e2.setValidator(QIntValidator())
      self.e2.setMaxLength(2)
      self.e1.setAlignment(Qt.AlignRight)

      self.flo = QFormLayout()
      self.flo.addRow("Total Output", self.e1)
      self.flo.addRow("Total Reject", self.e2)
      layout.addLayout(self.flo)

      #Date Sprayed
      self.calender = QCalendarWidget()
      layout.addWidget(self.calender)

      self.b1 = QPushButton("Submit")
      self.b1.setCheckable(True)
      self.b1.clicked.connect(self.confirmation)
      layout.addWidget(self.b1)

      self.setLayout(layout)

   def confirmation(self):
       
       part_code = self.part_code_entry.currentText()
       spray_output_amount = self.e1.text()
       spray_output_rejected = self.e2.text()
       date_sprayed = self.calender.selectedDate().toString("yyyy-MM-dd")

       msg = QMessageBox()
       msg.setIcon(QMessageBox.Information)
       msg.setText("Please confirm entered values")
       msg.setInformativeText(f"""
        Part Code: {part_code}
        Total Sprayed: {spray_output_amount}
        Total Rejected: {spray_output_rejected}
        Date Sprayed: {date_sprayed}
         """)
       
       msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
       msg.buttonClicked.connect(self.submit_new_spray_batch)
       retval = msg.exec_()

       

   def submit_new_spray_batch(self):
      # Get the selected part code and other input values
      part_code = self.part_code_entry.currentText()
      spray_output_amount = self.e1.text()
      spray_output_rejected = self.e2.text()
      date_sprayed = self.calender.selectedDate().toString("yyyy-MM-dd")

      try:
         # Start a transaction
         my_cursor.execute("START TRANSACTION;")

         # Get part_name and parent_id for the selected part_code
         my_cursor.execute(
               "SELECT part_name, parent_id FROM main_parts WHERE part_code = %s", 
               (part_code,)
         )
         result = my_cursor.fetchone()

         if result:
               part_name, parent_id = result
         else:
               print("No matching part found for the given part code.")
               return  # Exit if no matching part is found

         # Prepare and execute the SQL query for insertion
         sql = """
               INSERT INTO unchecked_spray 
               (part_name, part_code, date_sprayed, spray_output_amount, spray_output_rejected, parent_id) 
               VALUES (%s, %s, %s, %s, %s, %s)
         """
         values = (part_name, part_code, date_sprayed, spray_output_amount, spray_output_rejected, parent_id)
         my_cursor.execute(sql, values)

         my_cursor.execute("SELECT LAST_INSERT_ID();")
         last_spray_batch_id = my_cursor.fetchone()[0]

         sql2 = """
                INSERT INTO spray_batch_info 
                (spray_batch_info.date_sprayed, part_name, part_code, parent_id, spray_batch_id, total_output, batch_status) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

         unchecked_spray_balance = int(spray_output_amount) - int(spray_output_rejected)
         val2 = (date_sprayed, part_name, part_code, parent_id, last_spray_batch_id, unchecked_spray_balance, 'incomplete')
         my_cursor.execute(sql2, val2)

         mydb.commit()  # Commit the changes to the database
         print("Record inserted successfully.")

         self.part_code_entry.setCurrentIndex(0)  # Reset the combo box to the first item
         self.e1.clear()  # Clear the total output QLineEdit
         self.e2.clear()  # Clear the total reject QLineEdit
         self.calender.setSelectedDate(QDate.currentDate())  # Reset the calendar to today's date
         print("Inputs cleared after submission.")
            

      except Exception as e:
            # Rollback the transaction on error
            my_cursor.execute("ROLLBACK;")
            print(f"Error: {e}")

class open_new_batch_print_window(QWidget):
   def __init__(self, part_codes, parent = None):
      super().__init__(parent)
      self.part_codes = part_codes

      self.setWindowTitle("Enter New Print Batch")
      layout = QHBoxLayout()
    
      self.b1 = QPushButton("New Print Batch")
      self.b1.setCheckable(True)
      self.b1.clicked.connect(self.new_print_batch_entry_window)
      layout.addWidget(self.b1)

      self.b2 = QPushButton("Take From Spray")
      self.b2.setCheckable(True)
      self.b2.clicked.connect(self.take_from_spray_entry_window)
      layout.addWidget(self.b2)

      self.setLayout(layout)

      self.new_print_batch_entry_window = None
      self.take_from_spray_entry_window = None
   
   def new_print_batch_entry_window(self):
      
      # Check if the spray_print window is already open; if not, create it
      if self.new_print_batch_entry_window is None:
         self.new_print_batch_entry_window = new_print_batch_entry_window(self.part_codes)
      
      # Show the new_print_batch_entry_window window
      self.new_print_batch_entry_window.show()

   def take_from_spray_entry_window(self):
      
      # Check if the spray_print window is already open; if not, create it
      if self.take_from_spray_entry_window is None:
         self.take_from_spray_entry_window = take_from_spray()
      
      # Show the take_from_spray_entry_window window
      self.take_from_spray_entry_window.show()
      
      

class new_print_batch_entry_window(QWidget):
    def __init__(self, part_codes, parent = None):
        super(new_print_batch_entry_window,self).__init__(parent)

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        grid = QGridLayout()
        
        #Part Code
        self.part_code_entry = ExtendedComboBox()
        self.part_code_entry.addItems(part_codes)
        vlayout.addWidget(self.part_code_entry)

        #Output amount
        self.e1 = QLineEdit()
        self.e1.setValidator(QIntValidator())
        self.e1.setMaxLength(4)
        self.e1.setAlignment(Qt.AlignRight)

        self.e2 = QLineEdit()
        name_validator = QRegExpValidator(QRegExp("[a-zA-Z ]+"))  # Regex to allow alphabets and spaces
        self.e2.setValidator(name_validator)
        self.e2.setMaxLength(30)  # Optional: Set maximum length
        self.e2.setAlignment(Qt.AlignLeft)
        self.e2.setPlaceholderText("Enter name (alphabets and spaces only)")

        
        self.cb1 = QCheckBox('Secondary Process')
        self.cb1.setChecked(False)
        vlayout.addWidget(self.cb1)

        self.flo = QFormLayout()
        self.flo.addRow("Total Output", self.e1)
        self.flo.addRow("Checker", self.e2)
        vlayout.addLayout(self.flo)

        #Date Printed
        self.calender = QCalendarWidget()
        vlayout.addWidget(self.calender)

        #Submit Button
        self.b1 = QPushButton("Submit")
        self.b1.setCheckable(True)
        self.b1.clicked.connect(self.confirmation)
        vlayout.addWidget(self.b1)
        #Defect Reasons

        #test

        self.reject_details = [
            "dust_mark", "under_spray", "scratches", "dented", "bubble", 
            "white_dot", "dust_paint", "sink_mark", "black_dot", "smear", 
            "dirty", "bulging", "short_mould", "weldline", "incompleted", 
            "colour_out", "gate_high", "over_stamp", "ink_mark", "banding", 
            "shining", "overtrim", "dprinting", "dust_fibre", "thiner_mark"
        ]

        self.spin_boxes = {}

        # Populate grid with labels and line edits
        for i, detail in enumerate(self.reject_details):
            label = QLabel(detail.replace('_', ' ').capitalize())
            spin_box = QSpinBox()
            spin_box.setRange(0, 100)  # Set range as needed
            self.spin_boxes[detail] = spin_box  # Store reference to each spin box

            grid.addWidget(label, i // 2, (i % 2) * 2)
            grid.addWidget(spin_box, i // 2, (i % 2) * 2 + 1)

        hlayout.addLayout(vlayout)
        hlayout.addLayout(grid)
        self.setLayout(hlayout)

    def clear_defect_details(self):
        # Clear all spin boxes in the reject details
        for spin_box in self.spin_boxes.values():
            spin_box.setValue(0)  # Reset each spin box value to 0

    def confirmation(self):
        part_code = self.part_code_entry.currentText()
        print_output_amount = self.e1.text()
        date_print = self.calender.selectedDate().toString("yyyy-MM-dd")
        checker = self.e2.text().upper()

        # Collect non-zero rejection details
        non_zero_defects = {detail: spin_box.value() for detail, spin_box in self.spin_boxes.items() if spin_box.value() > 0}

        # Format non-zero rejection details for display using HTML for better alignment
        rejection_details_text = "<br>".join([f"{detail.replace('_', ' ').capitalize()}: {value}" for detail, value in non_zero_defects.items()])

        # Set up the confirmation message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Please confirm entered values")
        msg.setInformativeText(
            f"<b>Part Code:</b> {part_code}<br>"
            f"<b>Total Printed:</b> {print_output_amount}<br>"
            f"<b>Total Rejected:</b> {sum(non_zero_defects.values())}<br>"
            f"<b>Date Printed:</b> {date_print}<br>"
            f"<b>Checker:</b> {checker}<br><br>"
            f"<b>Rejection Details:</b><br>{rejection_details_text if rejection_details_text else 'None'}"
        )
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # Capture the button clicked and proceed with submission only if OK is clicked
        if msg.exec_() == QMessageBox.Ok:
            self.submit_new_print_batch()

    def submit_new_print_batch(self):
        
      part_code = self.part_code_entry.currentText()
      print_output_amount = self.e1.text()
      date_print = self.calender.selectedDate().toString("yyyy-MM-dd")
      total_defects = 0
      defect_data = {}
      checker = self.e2.text().upper()

      try:
         # Start a transaction
         my_cursor.execute("START TRANSACTION;")

         # Fetch part_name and parent_id based on the entered part code
         my_cursor.execute(
            "SELECT part_name, parent_id FROM main_parts WHERE part_code = %s",
            (part_code,)
         )
         result = my_cursor.fetchone()

        # Collect defect data from spin boxes
         for defect, spin_box in self.spin_boxes.items():
             defect_data[defect] = spin_box.value()
             total_defects += spin_box.value()  # Sum up total defects

         if not result:
            print("No matching part found for the given part code.")
            mydb.rollback()  # Rollback if no matching part
            return
         
         part_name, parent_id = result

         # Insert into `print_batch_info` and fetch `print_info_id`
         sql_print_batch_info = """
         INSERT INTO print_batch_info 
         (part_name, part_code, parent_id, date_printed, batch_status)
         VALUES (%s, %s, %s, %s, %s)
         """
         print_batch_input = (
            part_name,
            part_code,
            parent_id,
            date_print,
            "incomplete"
         )
         my_cursor.execute(sql_print_batch_info, print_batch_input)

         # Fetch the newly generated `print_info_id`
         my_cursor.execute("SELECT LAST_INSERT_ID();")
         last_print_info_id = my_cursor.fetchone()[0]

         if self.cb1.isChecked():
            # Insert into `history_print` table
            sql_print_history = """
                INSERT INTO history_print
                (date_print, part_name, part_code, amount_inspect, amount_reject, parent_id, print_info_id, movement_reason, checker_name, date_entered) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            print_history_inputs = (
                date_print,
                part_name,
                part_code,
                print_output_amount,
                total_defects if total_defects is not None else 0,
                parent_id,
                last_print_info_id,  # Using the fetched `print_info_id`
                "Secondary process",
                checker
            )
         else:
            sql_print_history = """
                INSERT INTO history_print
                (date_print, part_name, part_code, amount_inspect, amount_reject, parent_id, print_info_id, movement_reason, checker_name, date_entered) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            print_history_inputs = (
                date_print,
                part_name,
                part_code,
                print_output_amount,
                total_defects if total_defects is not None else 0,
                parent_id,
                last_print_info_id,  # Using the fetched `print_info_id`
                "New print batch",
                checker
            )
         
         my_cursor.execute(sql_print_history, print_history_inputs)


         # Fetch the last inserted `print_inspection_id`
         my_cursor.execute("SELECT LAST_INSERT_ID();")
         last_print_inspection_id = my_cursor.fetchone()[0]

         # Insert into `print_defect_list` using `last_print_inspection_id`
         sql = """
            INSERT INTO print_defect_list (print_inspection_id, dust_mark, under_spray, scratches, dented, bubble, 
            white_dot, dust_paint, sink_mark, black_dot, smear, dirty, bulging, short_mould, 
            weldline, incompleted, colour_out, gate_high, over_stamp, ink_mark, banding, 
            shining, overtrim, dprinting, dust_fibre, thiner_mark)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
         """
         values = (last_print_inspection_id,) + tuple(defect_data.get(defect, 0) for defect in self.reject_details) 
         my_cursor.execute(sql, values)

         # Commit to finalize the `print_defect_list` insert
         mydb.commit()
         print("Data Inserted")
         self.e1.clear()  # Clear the total output QLineEdit
         self.e2.clear()  # Clear the total output QLineEdit
         self.calender.setSelectedDate(QDate.currentDate())  # Reset the calendar to today's date
         self.clear_defect_details()

      except mysql.connector.Error as e:
         mydb.rollback()  # Roll back transaction in case of an error
         print(f"Error: {e}")

class take_from_spray(QWidget):
    # Define the signal that will be emitted
    part_selected = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super(take_from_spray, self).__init__(parent)
        self.resize(1000, 500)

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        grid = QGridLayout()

        self.calender = QCalendarWidget()
        vlayout.addWidget(self.calender)
        self.calender.clicked[QDate].connect(self.load_parts_for_date)

        self.listWidget = QListWidget()
        vlayout.addWidget(self.listWidget)
        # Connect the itemClicked signal to the on_item_clicked function
        self.listWidget.itemClicked.connect(self.on_item_clicked)

        self.selected_part_label = QLabel("Selected Part Name:")
        vlayout.addWidget(self.selected_part_label)

        self.setLayout(vlayout)

        self.load_parts_for_date(self.calender.selectedDate())
        self.open_entry_form_instance = None  # Renamed to avoid conflict with method name

    def load_parts_for_date(self, selected_date):
        # Clear the list widget to refresh with new data
        self.listWidget.clear()

        # Convert QDate to string in format 'YYYY-MM-DD'
        date_str = selected_date.toString("yyyy-MM-dd")

        # Fetch data for the selected date
        query = """
            SELECT spray_batch_id, part_code, part_name, hundered_balance 
            FROM spray_batch_info 
            WHERE date_sprayed = %s
        """
        my_cursor.execute(query, (date_str,))
        part_list = my_cursor.fetchall()

        # Populate list widget with parts information
        for spray_batch_id, part_code, part_name, hundered_balance in part_list:
            part_info = f"Spray Batch ID: {spray_batch_id}, Part Name: {part_name}, Part Code: {part_code}, Balance: {hundered_balance}"
            self.listWidget.addItem(part_info)

    def on_item_clicked(self, item):
        # Parse the spray ID and part code from the selected item text
        item_text = item.text()
        spray_id = item_text.split(",")[0].split(":")[1].strip()
        part_code = item_text.split(",")[2].split(":")[1].strip()

        # Emit the signal and open the entry form with parsed spray_id and part_code
        self.part_selected.emit(int(spray_id), part_code)  # Emit the signal

        # Optionally, call open_entry_form
        self.open_entry_form(spray_id, part_code)

    def open_entry_form(self, spray_id, part_code):
        # Check if the window is already open; if not, create it
        if self.open_entry_form_instance is None:
            self.open_entry_form_instance = open_take_from_spray_entry(spray_id, part_code)
        
        # Update the part label if the form is already open
        else:
            self.open_entry_form_instance.spray_id = spray_id
            self.open_entry_form_instance.part_code = part_code
            self.open_entry_form_instance.selected_part_label.setText(f"Selected Part Code: {part_code}")

        # Show the window
        self.open_entry_form_instance.show()


class open_take_from_spray_entry(QWidget):
    def __init__(self, spray_id, part_code, parent=None):
        super(open_take_from_spray_entry, self).__init__(parent)

        self.spray_id = spray_id
        self.part_code = part_code

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        grid = QGridLayout()

        # Output amount
        self.selected_part_label = QLabel(f"Selected Part Code: {part_code}")
        vlayout.addWidget(self.selected_part_label)
        
        self.e1 = QLineEdit()
        self.e1.setValidator(QIntValidator())
        self.e1.setMaxLength(4)
        self.e1.setAlignment(Qt.AlignRight)

        self.e2 = QLineEdit()
        name_validator = QRegExpValidator(QRegExp("[a-zA-Z ]+"))  # Regex to allow alphabets and spaces
        self.e2.setValidator(name_validator)
        self.e2.setMaxLength(30)  # Optional: Set maximum length
        self.e2.setAlignment(Qt.AlignLeft)
        self.e2.setPlaceholderText("Enter name (alphabets and spaces only)")

        self.cb1 = QCheckBox('Secondary Process')
        self.cb1.setChecked(False)
        vlayout.addWidget(self.cb1)

        # self.cb1 = QCheckBox()
        # self.cb1.setchecked(False)

        self.flo = QFormLayout()
        self.flo.addRow("Total Output", self.e1)
        self.flo.addRow("Checker", self.e2)
        vlayout.addLayout(self.flo)

        
        

        # Date Printed
        self.calender = QCalendarWidget()
        vlayout.addWidget(self.calender)

        # Submit Button
        self.b1 = QPushButton("Submit")
        self.b1.setCheckable(True)
        self.b1.clicked.connect(self.confirmation)
        vlayout.addWidget(self.b1)

        # Defect details with spin boxes
        self.reject_details = {
            "dust_marks", "under_spray", "scratches", "dented", "bubble", "dust_paint", "sink_mark", "black_dot", "white_dot",
            "smear", "dirty", "bulging", "short_mould", "weldline", "incompleted", "colour_out", "gate_high", "over_stamp",
            "ink_mark", "banding", "shining", "overtrim", "dprinting", "dust_fibre", "thiner_mark", "position_out", "adjustment"
        }
        
        self.spin_boxes = {}

        # Populate grid with labels and spin boxes
        for i, detail in enumerate(self.reject_details):
            label = QLabel(detail.replace('_', ' ').capitalize())
            spin_box = QSpinBox()
            spin_box.setRange(0, 100)  # Set range as needed
            self.spin_boxes[detail] = spin_box  # Store reference to each spin box

            grid.addWidget(label, i // 2, (i % 2) * 2)
            grid.addWidget(spin_box, i // 2, (i % 2) * 2 + 1)

        hlayout.addLayout(vlayout)
        hlayout.addLayout(grid)
        self.setLayout(hlayout)

    def clear_defect_details(self):
        # Clear all spin boxes in the reject details
        for spin_box in self.spin_boxes.values():
            spin_box.setValue(0)  # Reset each spin box value to 0

    def confirmation(self):
        part_code = self.part_code
        print_output_amount = self.e1.text()
        date_print = self.calender.selectedDate().toString("yyyy-MM-dd")
        checker = self.e2.text().upper()

        # Collect non-zero rejection details
        non_zero_defects = {detail: spin_box.value() for detail, spin_box in self.spin_boxes.items() if spin_box.value() > 0}

        # Format non-zero rejection details for display using HTML for better alignment
        rejection_details_text = "<br>".join([f"{detail.replace('_', ' ').capitalize()}: {value}" for detail, value in non_zero_defects.items()])

        # Set up the confirmation message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Please confirm entered values")
        msg.setInformativeText(
            f"<b>Part Code:</b> {part_code}<br>"
            f"<b>Total Printed:</b> {print_output_amount}<br>"
            f"<b>Total Rejected:</b> {sum(non_zero_defects.values())}<br>"
            f"<b>Date Printed:</b> {date_print}<br>"
            f"<b>Checker:</b> {checker}<br><br>"
            f"<b>Rejection Details:</b><br>{rejection_details_text if rejection_details_text else 'None'}"
        )
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # Capture the button clicked and proceed with submission only if OK is clicked
        if msg.exec_() == QMessageBox.Ok:
            self.submit_take_from_spray()

   
    def submit_take_from_spray(self):

      date_print = self.calender.selectedDate().toString("yyyy-MM-dd")
      print_output_amount = self.e1.text()
      defect_data = {}
      total_defects = 0
      checker = self.e2.text().upper()

      try:
         # Start a transaction
         my_cursor.execute("START TRANSACTION;")
         
         # Fetch part_name and parent_id based on the entered part code
         my_cursor.execute(
               "SELECT part_name, parent_id FROM main_parts WHERE part_code = %s", 
               (self.part_code,)
         )

         result = my_cursor.fetchone()

         # Collect defect data from spin boxes
         for defect, spin_box in self.spin_boxes.items():
             defect_data[defect] = spin_box.value()
             total_defects += spin_box.value()  # Sum up total defects

         if result:
               part_name, parent_id = result
         else:
               print("No matching part found for the given part code.")
               my_cursor.execute("ROLLBACK;")  # Rollback if no matching part
               return
         
         # Check if `spray_batch_id` exists in `print_batch_info`
         my_cursor.execute(
                "SELECT print_info_id FROM print_batch_info WHERE spray_batch_id = %s",
                (self.spray_id,)
            )
         result = my_cursor.fetchone()



         if result:
                # If batch exists, use the existing print_info_id
                last_print_info_id = result[0]
                print("Batch exists, using existing print_info_id:", last_print_info_id)
         else:
                # Insert into `print_batch_info` as the entry doesn't exist
                sql_print_batch_info = """
                INSERT INTO print_batch_info 
                (part_name, part_code, parent_id, spray_batch_id, date_printed, batch_status)
                VALUES (%s, %s, %s, %s, %s, %s)
                """

                print_batch_input = (
                    part_name,
                    self.part_code,
                    parent_id,
                    self.spray_id,
                    date_print,
                    "incomplete"
                )

                # Now execute the insertion
                my_cursor.execute(sql_print_batch_info, print_batch_input)

                # Retrieve the new print_info_id
                my_cursor.execute("SELECT LAST_INSERT_ID();")
                last_print_info_id = my_cursor.fetchone()[0]
                print("Inserted new row into print_batch_info with print_info_id:", last_print_info_id)

         if self.cb1.isChecked():
            # Insert into `history_print` table
            sql_print_history = """
                INSERT INTO history_print
                (date_print, part_name, part_code, amount_inspect, amount_reject, parent_id, print_info_id, movement_reason, checker_name, date_entered) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            print_history_inputs = (
                date_print,
                part_name,
                self.part_code,
                print_output_amount,
                total_defects if total_defects is not None else 0,
                parent_id,
                last_print_info_id,  # Using the fetched `print_info_id`
                "Secondary process",
                checker
            )
         else:
            sql_print_history = """
                INSERT INTO history_print
                (date_print, part_name, part_code, amount_inspect, amount_reject, parent_id, print_info_id, movement_reason, checker_name, date_entered) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            print_history_inputs = (
                date_print,
                part_name,
                self.part_code,
                print_output_amount,
                total_defects if total_defects is not None else 0,
                parent_id,
                last_print_info_id,  # Using the fetched `print_info_id`
                "New print batch",
                checker
            )
         my_cursor.execute(sql_print_history, print_history_inputs)

         # Retrieve the new print_inspection_id
         my_cursor.execute("SELECT LAST_INSERT_ID();")
         last_print_inspection_id = my_cursor.fetchone()[0]

         # Insert into `history_spray` table
         sql_spray_history = """
         INSERT INTO history_spray
         (movement_date, part_name, part_code, amount_inspect, amount_reject, parent_id, spray_batch_id, movement_reason, checker_name, date_entered) 
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
         """
         spray_history_inputs = (
         date_print,
         part_name,
         self.part_code,
         print_output_amount,
         total_defects,
         parent_id,
         self.spray_id,
         "print",
         checker
         )
         my_cursor.execute(sql_spray_history, spray_history_inputs)
         my_cursor.execute("SELECT LAST_INSERT_ID();")
         last_spray_inspection_id = my_cursor.fetchone()[0]

         # Insert defects into `print_defect_list` using the correct `print_inspection_id`
         sql_defect_list = """
         INSERT INTO print_defect_list
         (print_inspection_id, dust_mark, under_spray, scratches, dented, bubble, dust_paint, 
         sink_mark, black_dot, white_dot, smear, dirty, bulging, short_mould, 
         weldline, incompleted, colour_out, gate_high, over_stamp, ink_mark, banding, shining,
         overtrim, dprinting, dust_fibre, thiner_mark, position_out, adjustment)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
         """

         values = (last_print_inspection_id,) + tuple(defect_data.get(defect, 0) for defect in self.reject_details) 
         my_cursor.execute(sql_defect_list, values)

         sql_spray_defect_list = """
            INSERT INTO spray_defect_list
            (spray_inspection_id, print_defects)
            VALUES(%s, %s)
            """
         values2 = (last_spray_inspection_id, total_defects if total_defects is not None else 0 )
         my_cursor.execute(sql_spray_defect_list, values2)


         # Commit to finalize the `print_defect_list` insert
         mydb.commit()
         print("Data Inserted")

         self.e1.clear()  # Clear the total output QLineEdit
         self.e2.clear()  # Clear the total output QLineEdit
         self.calender.setSelectedDate(QDate.currentDate())  # Reset the calendar to today's date
         self.clear_defect_details()

      except mysql.connector.Error as e:
         mydb.rollback()  # Roll back transaction in case of an error
         print(f"Error: {e}")

class first_phase_checking(QWidget):

    part_selected = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super(first_phase_checking, self).__init__(parent)
        self.resize(1000, 500)

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        grid = QGridLayout()

        self.calender = QCalendarWidget()
        vlayout.addWidget(self.calender)
        self.calender.clicked[QDate].connect(self.load_parts_for_date)

        self.listWidget = QListWidget()
        vlayout.addWidget(self.listWidget)
        # Connect the itemClicked signal to the on_item_clicked function
        self.listWidget.itemClicked.connect(self.on_item_clicked)

        self.selected_part_label = QLabel("Selected Part Name:")
        vlayout.addWidget(self.selected_part_label)

        self.setLayout(vlayout)

        self.load_parts_for_date(self.calender.selectedDate())
        self.open_entry_form_instance = None  # Renamed to avoid conflict with method name

    def load_parts_for_date(self, selected_date):
        # Clear the list widget to refresh with new data
        self.listWidget.clear()

        # Convert QDate to string in format 'YYYY-MM-DD'
        date_str = selected_date.toString("yyyy-MM-dd")

        # Fetch data for the selected date
        query = """
            SELECT spray_batch_id, part_code, part_name, unchecked_balance, total_output 
            FROM spray_batch_info 
            WHERE date_sprayed = %s
        """
        my_cursor.execute(query, (date_str,))
        part_list = my_cursor.fetchall()

        # Populate list widget with parts information
        for spray_batch_id, part_code, part_name, unchecked_balance, total_output in part_list:
            # Use total_output as unchecked_balance if unchecked_balance is None
            display_balance = unchecked_balance if unchecked_balance is not None else total_output
            part_info = f"Spray Batch ID: {spray_batch_id}, Part Name: {part_name}, Part Code: {part_code}, Unchecked Balance: {display_balance}"
            self.listWidget.addItem(part_info)


    def on_item_clicked(self, item):
         # Parse the spray ID and part code from the selected item text
         item_text = item.text()
         spray_id = item_text.split(",")[0].split(":")[1].strip()
         part_code = item_text.split(",")[2].split(":")[1].strip()

         # Emit the signal and open the entry form with parsed spray_id and part_code
         self.part_selected.emit(int(spray_id), part_code)  # Emit the signal

         # Optionally, call open_entry_form
         self.open_entry_form(spray_id, part_code)

    def open_entry_form(self, spray_id, part_code):
         # Check if the window is already open; if not, create it
         if self.open_entry_form_instance is None:
               self.open_entry_form_instance = open_first_phase_checking_entry(spray_id, part_code)
         
         # Update the part label if the form is already open
         else:
               self.open_entry_form_instance.spray_id = spray_id
               self.open_entry_form_instance.part_code = part_code
               self.open_entry_form_instance.selected_part_label.setText(f"Selected Part Code: {part_code}")

         # Show the window
         self.open_entry_form_instance.show()

class open_first_phase_checking_entry(QWidget):
      def __init__(self, spray_id, part_code, parent=None):
         super(open_first_phase_checking_entry, self).__init__(parent)

         self.spray_id = spray_id
         self.part_code = part_code

         vlayout = QVBoxLayout()
         hlayout = QHBoxLayout()
         grid = QGridLayout()

         # Output amount
         self.selected_part_label = QLabel(f"Selected Part Code: {part_code}")
         vlayout.addWidget(self.selected_part_label)
         
         self.e1 = QLineEdit()
         self.e1.setValidator(QIntValidator())
         self.e1.setMaxLength(4)
         self.e1.setAlignment(Qt.AlignRight)

         self.e2 = QLineEdit()
         name_validator = QRegExpValidator(QRegExp("[a-zA-Z ]+"))  # Regex to allow alphabets and spaces
         self.e2.setValidator(name_validator)
         self.e2.setMaxLength(30)  # Optional: Set maximum length
         self.e2.setAlignment(Qt.AlignLeft)
         self.e2.setPlaceholderText("Enter name (alphabets and spaces only)")

         self.flo = QFormLayout()
         self.flo.addRow("Total Checked", self.e1)
         self.flo.addRow("Checker", self.e2)
         vlayout.addLayout(self.flo)

         # Date Printed
         self.calender = QCalendarWidget()
         vlayout.addWidget(self.calender)

         # Submit Button
         self.b1 = QPushButton("Submit")
         self.b1.setCheckable(True)
         self.b1.clicked.connect(self.confirmation)
         vlayout.addWidget(self.b1)

         # Defect details with spin boxes
         self.reject_details = {
                "dust_marks","fibre_marks","paint_marks","white_marks","sink_marks","texture_marks","water_marks",
                "flow_marks","black_dot","white_dot","over_paint","under_spray","colour_out","masking_ng","flying_paint","weldline",
                "banding","short_mould","sliver_streak","dented","scratches","dirty"
            }
         self.spin_boxes = {}

         # Populate grid with labels and spin boxes
         for i, detail in enumerate(self.reject_details):
               label = QLabel(detail.replace('_', ' ').capitalize())
               spin_box = QSpinBox()
               spin_box.setRange(0, 100)  # Set range as needed
               self.spin_boxes[detail] = spin_box  # Store reference to each spin box

               grid.addWidget(label, i // 2, (i % 2) * 2)
               grid.addWidget(spin_box, i // 2, (i % 2) * 2 + 1)

         hlayout.addLayout(vlayout)
         hlayout.addLayout(grid)
         self.setLayout(hlayout)

      def confirmation(self):
        part_code = self.part_code
        checked_output_amount = self.e1.text()
        date_checked = self.calender.selectedDate().toString("yyyy-MM-dd")
        checker = self.e2.text().upper()

        # Collect non-zero rejection details
        non_zero_defects = {detail: spin_box.value() for detail, spin_box in self.spin_boxes.items() if spin_box.value() > 0}

        # Format non-zero rejection details for display using HTML for better alignment
        rejection_details_text = "<br>".join([f"{detail.replace('_', ' ').capitalize()}: {value}" for detail, value in non_zero_defects.items()])

        # Set up the confirmation message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Please confirm entered values")
        msg.setInformativeText(
            f"<b>Part Code:</b> {part_code}<br>"
            f"<b>Total Checked:</b> {checked_output_amount}<br>"
            f"<b>Total Rejected:</b> {sum(non_zero_defects.values())}<br>"
            f"<b>Date Checked:</b> {date_checked}<br>"
            f"<b>Checker:</b> {checker}<br><br>"
            f"<b>Rejection Details:</b><br>{rejection_details_text if rejection_details_text else 'None'}"
        )
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # Capture the button clicked and proceed with submission only if OK is clicked
        if msg.exec_() == QMessageBox.Ok:
            self.submit_first_phase_check()

      def clear_defect_details(self):
        # Clear all spin boxes in the reject details
        for spin_box in self.spin_boxes.values():
         spin_box.setValue(0)  # Reset each spin box value to 0

      
      def submit_first_phase_check(self):
        date_checked = self.calender.selectedDate().toString("yyyy-MM-dd")
        checked_output_amount = self.e1.text()
        defect_data = {}
        total_defects = 0
        checker = self.e2.text().upper()

        try:
            # Start a transaction
            my_cursor.execute("START TRANSACTION;")
            
            # Fetch part_name and parent_id based on the entered part code
            my_cursor.execute(
                "SELECT part_name, parent_id FROM main_parts WHERE part_code = %s", 
                (self.part_code,)
            )
            result = my_cursor.fetchone()
            if result:
                part_name, parent_id = result
            else:
                print("No matching part found for the given part code.")
                my_cursor.execute("ROLLBACK;")  # Rollback if no matching part
                return

            # Check if `spray_batch_id` exists in `print_batch_info`
            my_cursor.execute(
                "SELECT print_info_id FROM print_batch_info WHERE spray_batch_id = %s",
                (self.spray_id,)
            )
            result = my_cursor.fetchone()

            # Collect defect data from spin boxes
            for defect, spin_box in self.spin_boxes.items():
                defect_data[defect] = spin_box.value()
                total_defects += spin_box.value()  # Sum up total defects

            # Insert into `history_spray` table
            sql_spray_history = """
                INSERT INTO history_spray
                (movement_date, part_name, part_code, amount_inspect, amount_reject, parent_id, spray_batch_id, movement_reason, checker_name, date_entered ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            spray_history_inputs = (
                date_checked,
                part_name,
                self.part_code,
                checked_output_amount,
                total_defects,  # Use calculated total defects
                parent_id,
                self.spray_id,
                "100",
                checker
            )
            my_cursor.execute(sql_spray_history, spray_history_inputs)
            my_cursor.execute("SELECT LAST_INSERT_ID();")
            last_spray_inspection_id = my_cursor.fetchone()[0]

            # Insert defects into `spray_defect_list` using the correct `spray_inspection_id`
            sql_defect_list = """
            INSERT INTO spray_defect_list
            (spray_inspection_id, dust_mark, fibre_mark, paint_marks, white_marks, sink_marks, texture_marks, water_marks,
            flow_marks, black_dot, white_dot, over_paint, under_spray, colour_out, masking_ng, flying_paint, weldline,
            banding, short_mould, sliver_streak, dented, scratches, dirty)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (last_spray_inspection_id,) + tuple(defect_data.get(defect, 0) for defect in self.reject_details)
            my_cursor.execute(sql_defect_list, values)

            # Commit to finalize the `spray_defect_list` insert
            mydb.commit()
            print("Data Inserted")

            self.e1.clear()  # Clear the total output QLineEdit
            self.e2.clear()  # Clear the total output QLineEdit
            self.calender.setSelectedDate(QDate.currentDate())  # Reset the calendar to today's date
            self.clear_defect_details()

        except mysql.connector.Error as e:
            mydb.rollback()  # Roll back transaction in case of an error
            print(f"Error: {e}")

class first_phase_checking_print(QWidget):

    part_selected = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super(first_phase_checking_print, self).__init__(parent)
        self.resize(1000, 500)

        vlayout = QVBoxLayout()

        self.calender = QCalendarWidget()
        vlayout.addWidget(self.calender)
        self.calender.clicked[QDate].connect(self.load_parts_for_date)

        self.listWidget = QListWidget()
        vlayout.addWidget(self.listWidget)
        # Connect the itemClicked signal to the on_item_clicked function
        self.listWidget.itemClicked.connect(self.on_item_clicked)

        self.selected_part_label = QLabel("Selected Part Name:")
        vlayout.addWidget(self.selected_part_label)

        self.setLayout(vlayout)

        self.load_parts_for_date(self.calender.selectedDate())
        self.open_entry_form_instance = None  # Renamed to avoid conflict with method name

    def load_parts_for_date(self, selected_date):
        # Clear the list widget to refresh with new data
        self.listWidget.clear()

        # Convert QDate to string in format 'YYYY-MM-DD'
        date_str = selected_date.toString("yyyy-MM-dd")

        # Fetch data for the selected date
        query = """
            SELECT print_info_id, part_code, part_name, secondary_process_balance, total_output
            FROM print_batch_info 
            WHERE date_printed = %s
        """
        my_cursor.execute(query, (date_str,))
        part_list = my_cursor.fetchall()

        # Populate list widget with parts information
        for print_info_id, part_code, part_name, secondary_process_balance, total_output in part_list:
            # Use total_output as unchecked_balance if unchecked_balance is None
            display_balance = secondary_process_balance if secondary_process_balance is not None else total_output
            part_info = f"Print Batch ID: {print_info_id}, Part Name: {part_name}, Part Code: {part_code}, Secondary Process Balance: {display_balance}"
            self.listWidget.addItem(part_info)


    def on_item_clicked(self, item):
         # Parse the spray ID and part code from the selected item text
         item_text = item.text()
         print_id = item_text.split(",")[0].split(":")[1].strip()
         part_code = item_text.split(",")[2].split(":")[1].strip()

         # Emit the signal and open the entry form with parsed spray_id and part_code
         self.part_selected.emit(int(print_id), part_code)  # Emit the signal

         # Optionally, call open_entry_form
         self.open_entry_form(print_id, part_code)

    def open_entry_form(self, print_id, part_code):
         # Check if the window is already open; if not, create it
         if self.open_entry_form_instance is None:
               self.open_entry_form_instance = open_first_phase_checking_print_entry(print_id, part_code)
         
         # Update the part label if the form is already open
         else:
               self.open_entry_form_instance.print_id = print_id
               self.open_entry_form_instance.part_code = part_code
               self.open_entry_form_instance.selected_part_label.setText(f"Selected Part Code: {part_code}")

         # Show the window
         self.open_entry_form_instance.show()

class open_first_phase_checking_print_entry(QWidget):
      def __init__(self, print_id, part_code, parent=None):
         super(open_first_phase_checking_print_entry, self).__init__(parent)

         self.print_id = print_id
         self.part_code = part_code

         vlayout = QVBoxLayout()
         hlayout = QHBoxLayout()
         grid = QGridLayout()

         # Output amount
         self.selected_part_label = QLabel(f"Selected Part Code: {part_code}")
         vlayout.addWidget(self.selected_part_label)
         
         self.e1 = QLineEdit()
         self.e1.setValidator(QIntValidator())
         self.e1.setMaxLength(4)
         self.e1.setAlignment(Qt.AlignRight)

         self.e2 = QLineEdit()
         name_validator = QRegExpValidator(QRegExp("[a-zA-Z ]+"))  # Regex to allow alphabets and spaces
         self.e2.setValidator(name_validator)
         self.e2.setMaxLength(30)  # Optional: Set maximum length
         self.e2.setAlignment(Qt.AlignLeft)
         self.e2.setPlaceholderText("Enter name (alphabets and spaces only)")

         self.flo = QFormLayout()
         self.flo.addRow("Total Checked", self.e1)
         self.flo.addRow("Checker", self.e2)
         vlayout.addLayout(self.flo)

         # Date Printed
         self.calender = QCalendarWidget()
         vlayout.addWidget(self.calender)

         # Submit Button
         self.b1 = QPushButton("Submit")
         self.b1.setCheckable(True)
         self.b1.clicked.connect(self.confirmation)
         vlayout.addWidget(self.b1)

         # Defect details with spin boxes
         self.reject_details = {
                "dust_marks", "under_spray", "scratches", "dented", "bubble", "dust_paint", "sink_mark", "black_dot", "white_dot",
            "smear", "dirty", "bulging", "short_mould", "weldline", "incompleted", "colour_out", "gate_high", "over_stamp",
            "ink_mark", "banding", "shining", "overtrim", "dprinting", "dust_fibre", "thiner_mark", "position_out", "adjustment"
            }
         self.spin_boxes = {}

         # Populate grid with labels and spin boxes
         for i, detail in enumerate(self.reject_details):
               label = QLabel(detail.replace('_', ' ').capitalize())
               spin_box = QSpinBox()
               spin_box.setRange(0, 100)  # Set range as needed
               self.spin_boxes[detail] = spin_box  # Store reference to each spin box

               grid.addWidget(label, i // 2, (i % 2) * 2)
               grid.addWidget(spin_box, i // 2, (i % 2) * 2 + 1)

         hlayout.addLayout(vlayout)
         hlayout.addLayout(grid)
         self.setLayout(hlayout)

      def confirmation(self):
        part_code = self.part_code
        checked_output_amount = self.e1.text()
        date_checked = self.calender.selectedDate().toString("yyyy-MM-dd")
        checker = self.e2.text().upper()

        # Collect non-zero rejection details
        non_zero_defects = {detail: spin_box.value() for detail, spin_box in self.spin_boxes.items() if spin_box.value() > 0}

        # Format non-zero rejection details for display using HTML for better alignment
        rejection_details_text = "<br>".join([f"{detail.replace('_', ' ').capitalize()}: {value}" for detail, value in non_zero_defects.items()])

        # Set up the confirmation message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Please confirm entered values")
        msg.setInformativeText(
            f"<b>Part Code:</b> {part_code}<br>"
            f"<b>Total Checked:</b> {checked_output_amount}<br>"
            f"<b>Total Rejected:</b> {sum(non_zero_defects.values())}<br>"
            f"<b>Date Checked:</b> {date_checked}<br>"
            f"<b>Checker:</b> {checker}<br><br>"
            f"<b>Rejection Details:</b><br>{rejection_details_text if rejection_details_text else 'None'}"
        )
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # Capture the button clicked and proceed with submission only if OK is clicked
        if msg.exec_() == QMessageBox.Ok:
            self.submit_first_phase_check()

      def clear_defect_details(self):
        # Clear all spin boxes in the reject details
        for spin_box in self.spin_boxes.values():
         spin_box.setValue(0)  # Reset each spin box value to 0

      
      def submit_first_phase_check(self):
        date_checked = self.calender.selectedDate().toString("yyyy-MM-dd")
        checked_output_amount = self.e1.text()
        defect_data = {}
        total_defects = 0
        checker = self.e2.text().upper()

        try:
            # Start a transaction
            my_cursor.execute("START TRANSACTION;")
            
            # Fetch part_name and parent_id based on the entered part code
            my_cursor.execute(
                "SELECT part_name, parent_id FROM main_parts WHERE part_code = %s", 
                (self.part_code,)
            )
            result = my_cursor.fetchone()
            
            if result:
                part_name, parent_id = result
            else:
                print("No matching part found for the given part code.")
                my_cursor.execute("ROLLBACK;")  # Rollback if no matching part
                return


            # Collect defect data from spin boxes
            for defect, spin_box in self.spin_boxes.items():
                defect_data[defect] = spin_box.value()
                total_defects += spin_box.value()  # Sum up total defects

            # Insert into `history_spray` table
            sql_print_history = """
                INSERT INTO history_print
                (date_print, part_name, part_code, amount_inspect, amount_reject, parent_id, print_info_id, movement_reason, checker_name, date_entered ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            print_history_inputs = (
                date_checked,
                part_name,
                self.part_code,
                checked_output_amount,
                total_defects,  # Use calculated total defects
                parent_id,
                self.print_id,
                "100",
                checker
            )
            my_cursor.execute(sql_print_history, print_history_inputs)
            my_cursor.execute("SELECT LAST_INSERT_ID();")
            last_print_inspection_id = my_cursor.fetchone()[0]

            # Insert defects into `print_defect_list` using the correct `spray_inspection_id`
            sql_defect_list = """
            INSERT INTO print_defect_list
            (print_inspection_id, dust_mark, under_spray, scratches ,dented ,bubble ,dust_paint, 
            sink_mark ,black_dot ,white_dot ,smear ,dirty ,bulging ,short_mould, 
            weldline ,incompleted ,colour_out ,gate_high ,over_stamp ,ink_mark ,banding, shining,
            overtrim ,dprinting ,dust_fibre ,thiner_mark,position_out, adjustment)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            values = (last_print_inspection_id,) + tuple(defect_data.get(defect, 0) for defect in self.reject_details)
            my_cursor.execute(sql_defect_list, values)

            # Commit to finalize the `print_defect_list` insert
            mydb.commit()
            print("Data Inserted")

            self.e1.clear()  # Clear the total output QLineEdit
            self.e2.clear()  # Clear the total output QLineEdit
            self.calender.setSelectedDate(QDate.currentDate())  # Reset the calendar to today's date
            self.clear_defect_details()

        except mysql.connector.Error as e:
            mydb.rollback()  # Roll back transaction in case of an error
            print(f"Error: {e}")


class finished_goods_checking(QWidget):
      def __init__(self, parent=None):
         super(finished_goods_checking, self).__init__(parent)

         hlayout = QHBoxLayout()
      
         self.b1 = QPushButton("Spray")
         self.b1.setChecked(True)
         self.b1.clicked.connect(self.open_finished_goods_spray)
         hlayout.addWidget(self.b1)
         
         self.b2 = QPushButton("Print")
         self.b2.setChecked(True)
         self.b2.clicked.connect(self.open_finished_goods_print)
         hlayout.addWidget(self.b2)

         self.setLayout(hlayout)
         self.open_finished_goods_spray_window = None
         self.open_finished_goods_print_window = None
      
      def open_finished_goods_spray (self):
          
        if self.open_finished_goods_spray_window is None:
            self.open_finished_goods_spray_window = finished_goods_spray()
        
        # Show the open_new_batch_print_window window
        self.open_finished_goods_spray_window.show()

      def open_finished_goods_print (self):
          
        if self.open_finished_goods_print_window is None:
            self.open_finished_goods_print_window = finished_goods_print()
        
        # Show the open_new_batch_print_window window
        self.open_finished_goods_print_window.show()

class finished_goods_spray(QWidget):
      part_selected = pyqtSignal(int, str)  # Move signal outside __init__

      def __init__(self, parent=None):
         super(finished_goods_spray, self).__init__(parent)

         self.resize(1000, 500)

         vlayout = QVBoxLayout()

         self.calender = QCalendarWidget()
         vlayout.addWidget(self.calender)
         self.calender.clicked[QDate].connect(self.load_parts_for_date)

         self.listWidget = QListWidget()
         vlayout.addWidget(self.listWidget)
         # Connect the itemClicked signal to the on_item_clicked function
         self.listWidget.itemClicked.connect(self.on_item_clicked)

         self.selected_part_label = QLabel("Selected Part Name:")
         vlayout.addWidget(self.selected_part_label)

         self.setLayout(vlayout)

         self.load_parts_for_date(self.calender.selectedDate())
         self.open_entry_form_instance = None
              
      def load_parts_for_date(self, selected_date):
   

         # Clear the list widget to refresh with new data
         self.listWidget.clear()

         # Convert QDate to string in format 'YYYY-MM-DD'
         date_str = selected_date.toString("yyyy-MM-dd")

         # Fetch data for the selected date
         query = """
               SELECT spray_batch_id, part_code, part_name, hundered_balance 
               FROM spray_batch_info 
               WHERE date_sprayed = %s
         """
         my_cursor.execute(query, (date_str,))
         part_list = my_cursor.fetchall()

         # Populate list widget with parts information
         for spray_batch_id, part_code, part_name, hundered_balance in part_list:
               part_info = f"Spray Batch ID: {spray_batch_id}, Part Name: {part_name}, Part Code: {part_code}, 100% Balance: {hundered_balance}"
               self.listWidget.addItem(part_info)

      def on_item_clicked(self, item):
         # Parse the spray ID and part code from the selected item text
         item_text = item.text()
         spray_id = item_text.split(",")[0].split(":")[1].strip()
         part_code = item_text.split(",")[2].split(":")[1].strip()

         # Emit the signal and open the entry form with parsed spray_id and part_code
         self.part_selected.emit(int(spray_id), part_code)  # Emit the signal

         # Optionally, call open_entry_form
         self.open_entry_form(spray_id, part_code)

      def open_entry_form(self, spray_id, part_code):
         # Check if the window is already open; if not, create it
         if self.open_entry_form_instance is None:
               self.open_entry_form_instance = open_final_phase_checking_spray_entry(spray_id, part_code)
         
         # Update the part label if the form is already open
         else:
               self.open_entry_form_instance.spray_id = spray_id
               self.open_entry_form_instance.part_code = part_code
               self.open_entry_form_instance.selected_part_label.setText(f"Selected Part Code: {part_code}")

         # Show the window
         self.open_entry_form_instance.show()

class open_final_phase_checking_spray_entry(QWidget):
      def __init__(self, spray_id, part_code, parent=None):
         super(open_final_phase_checking_spray_entry, self).__init__(parent)

         self.spray_id = spray_id
         self.part_code = part_code

         vlayout = QVBoxLayout()
         hlayout = QHBoxLayout()
         grid = QGridLayout()

         # Output amount
         self.selected_part_label = QLabel(f"Selected Part Code: {part_code}")
         vlayout.addWidget(self.selected_part_label)
         
         self.e1 = QLineEdit()
         self.e1.setValidator(QIntValidator())
         self.e1.setMaxLength(4)
         self.e1.setAlignment(Qt.AlignRight)

         self.e2 = QLineEdit()
         name_validator = QRegExpValidator(QRegExp("[a-zA-Z ]+"))  # Regex to allow alphabets and spaces
         self.e2.setValidator(name_validator)
         self.e2.setMaxLength(30)  # Optional: Set maximum length
         self.e2.setAlignment(Qt.AlignLeft)
         self.e2.setPlaceholderText("Enter name (alphabets and spaces only)")

         self.flo = QFormLayout()
         self.flo.addRow("Total Checked", self.e1)
         self.flo.addRow("Checker", self.e2)
         vlayout.addLayout(self.flo)

         # Date Printed
         self.calender = QCalendarWidget()
         vlayout.addWidget(self.calender)

         # Submit Button
         self.b1 = QPushButton("Submit")
         self.b1.setCheckable(True)
         self.b1.clicked.connect(self.confirmation)
         vlayout.addWidget(self.b1)

         # Defect details with spin boxes
         self.reject_details = {
                "dust_marks","fibre_marks","paint_marks","white_marks","sink_marks","texture_marks","water_marks",
                "flow_marks","black_dot","white_dot","over_paint","under_spray","colour_out","masking_ng","flying_paint","weldline",
                "banding","short_mould","sliver_streak","dented","scratches","dirty"
            }
         self.spin_boxes = {}

         # Populate grid with labels and spin boxes
         for i, detail in enumerate(self.reject_details):
               label = QLabel(detail.replace('_', ' ').capitalize())
               spin_box = QSpinBox()
               spin_box.setRange(0, 100)  # Set range as needed
               self.spin_boxes[detail] = spin_box  # Store reference to each spin box

               grid.addWidget(label, i // 2, (i % 2) * 2)
               grid.addWidget(spin_box, i // 2, (i % 2) * 2 + 1)

         hlayout.addLayout(vlayout)
         hlayout.addLayout(grid)
         self.setLayout(hlayout)

      def clear_defect_details(self):
        # Clear all spin boxes in the reject details
        for spin_box in self.spin_boxes.values():
            spin_box.setValue(0)  # Reset each spin box value to 0

      
      def confirmation(self):
        part_code = self.part_code
        checked_output_amount = self.e1.text()
        date_checked = self.calender.selectedDate().toString("yyyy-MM-dd")
        checker = self.e2.text().upper()

        # Collect non-zero rejection details
        non_zero_defects = {detail: spin_box.value() for detail, spin_box in self.spin_boxes.items() if spin_box.value() > 0}

        # Format non-zero rejection details for display using HTML for better alignment
        rejection_details_text = "<br>".join([f"{detail.replace('_', ' ').capitalize()}: {value}" for detail, value in non_zero_defects.items()])

        # Set up the confirmation message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Please confirm entered values")
        msg.setInformativeText(
            f"<b>Part Code:</b> {part_code}<br>"
            f"<b>Total Checked:</b> {checked_output_amount}<br>"
            f"<b>Total Rejected:</b> {sum(non_zero_defects.values())}<br>"
            f"<b>Date Checked:</b> {date_checked}<br>"
            f"<b>Checker:</b> {checker}<br><br>"
            f"<b>Rejection Details:</b><br>{rejection_details_text if rejection_details_text else 'None'}"
        )
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # Capture the button clicked and proceed with submission only if OK is clicked
        if msg.exec_() == QMessageBox.Ok:
            self.submit_final_phase_check()


      
  
      def submit_final_phase_check(self):

         date_checked = self.calender.selectedDate().toString("yyyy-MM-dd")
         checked_output_amount = self.e1.text()
         defect_data = {}
         total_defects = 0
         checker = self.e2.text().upper()

         try:
            # Start a transaction
            my_cursor.execute("START TRANSACTION;")
            
            # Fetch part_name and parent_id based on the entered part code
            my_cursor.execute(
                  "SELECT part_name, parent_id FROM main_parts WHERE part_code = %s", 
                  (self.part_code,)
            )

            result = my_cursor.fetchone()

            # Collect defect data from spin boxes
            for defect, spin_box in self.spin_boxes.items():
                defect_data[defect] = spin_box.value()
                total_defects += spin_box.value()  # Sum up total defects

            if result:
                  part_name, parent_id = result
            else:
                  print("No matching part found for the given part code.")
                  my_cursor.execute("ROLLBACK;")  # Rollback if no matching part
                  return
            
            # Check if `spray_batch_id` exists in `print_batch_info`
            my_cursor.execute(
                  "SELECT print_info_id FROM print_batch_info WHERE spray_batch_id = %s",
                  (self.spray_id,)
            )
            result = my_cursor.fetchone()

            # Insert into `history_print` table
            sql_spray_history = """
                INSERT INTO history_spray
                (movement_date, part_name, part_code, amount_inspect, amount_reject, parent_id, spray_batch_id, movement_reason, checker_name, date_entered ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            spray_history_inputs = (
                date_checked,
                part_name,
                self.part_code,
                checked_output_amount,
                total_defects if total_defects is not None else 0, ### problem here
                parent_id,
                self.spray_id,
                "200",
                checker
            )

            """
            so here is insert into spray history first
            """
            my_cursor.execute(sql_spray_history, spray_history_inputs)
            my_cursor.execute("SELECT LAST_INSERT_ID();")
            last_spray_inspection_id = my_cursor.fetchone()[0]

            # Insert defects into `print_defect_list` using the correct `print_inspection_id`
            sql_defect_list = """
            INSERT INTO spray_defect_list
            (spray_inspection_id, dust_mark, fibre_mark, paint_marks, white_marks, sink_marks, texture_marks, water_marks,
            flow_marks, black_dot, white_dot, over_paint, under_spray, colour_out, masking_ng, flying_paint, weldline,
            banding, short_mould, sliver_streak, dented, scratches, dirty)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """

            values = (last_spray_inspection_id,) + tuple(defect_data.get(defect, 0) for defect in self.reject_details) 
            my_cursor.execute(sql_defect_list, values)

            # Commit to finalize the `print_defect_list` insert
            mydb.commit()
            print("Data Inserted")

            self.e1.clear()  # Clear the total output QLineEdit
            self.e2.clear()  # Clear the total output QLineEdit
            self.calender.setSelectedDate(QDate.currentDate())  # Reset the calendar to today's date
            self.clear_defect_details()

         except mysql.connector.Error as e:
            mydb.rollback()  # Roll back transaction in case of an error
            print(f"Error: {e}")

class finished_goods_print(QWidget):
    part_selected = pyqtSignal(int, str)  # Move signal outside __init__

    def __init__(self, parent=None):
        super(finished_goods_print, self).__init__(parent)

        self.resize(1000, 500)
        vlayout = QVBoxLayout()

        self.calender = QCalendarWidget()
        vlayout.addWidget(self.calender)
        self.calender.clicked[QDate].connect(self.load_parts_for_date)

        self.listWidget = QListWidget()
        vlayout.addWidget(self.listWidget)
        self.listWidget.itemClicked.connect(self.on_item_clicked)

        self.selected_part_label = QLabel("Selected Part Name:")
        vlayout.addWidget(self.selected_part_label)

        self.setLayout(vlayout)
        self.load_parts_for_date(self.calender.selectedDate())
        self.open_entry_form_instance = None

    def load_parts_for_date(self, selected_date):
        self.listWidget.clear()
        date_str = selected_date.toString("yyyy-MM-dd")

        query = """
            SELECT print_info_id, part_code, part_name, hundered_balance 
            FROM print_batch_info 
            WHERE date_printed = %s
        """
        my_cursor.execute(query, (date_str,))
        part_list = my_cursor.fetchall()

        for print_info_id, part_code, part_name, hundered_balance in part_list:
            part_info = f"Print Batch ID: {print_info_id}, Part Name: {part_name}, Part Code: {part_code}, 100% Balance: {hundered_balance}"
            self.listWidget.addItem(part_info)

    def on_item_clicked(self, item):
        item_text = item.text()
        print_id = int(item_text.split(",")[0].split(":")[1].strip())
        part_code = item_text.split(",")[2].split(":")[1].strip()

        self.part_selected.emit(print_id, part_code)  # Emit the signal
        self.open_entry_form(print_id, part_code)

    def open_entry_form(self, print_id, part_code):
        if self.open_entry_form_instance is None:
            self.open_entry_form_instance = open_final_phase_checking_entry(print_id, part_code)
        else:
            self.open_entry_form_instance.print_id = print_id
            self.open_entry_form_instance.part_code = part_code
            self.open_entry_form_instance.selected_part_label.setText(f"Selected Part Code: {part_code}")
        
        self.open_entry_form_instance.show()


class open_final_phase_checking_entry(QWidget):
    def __init__(self, print_id, part_code, parent=None):
        super(open_final_phase_checking_entry, self).__init__(parent)  # Use correct class name

        self.print_id = print_id
        self.part_code = part_code

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        grid = QGridLayout()

        self.selected_part_label = QLabel(f"Selected Part Code: {part_code}")
        vlayout.addWidget(self.selected_part_label)
        
        self.e1 = QLineEdit()
        self.e1.setValidator(QIntValidator())
        self.e1.setMaxLength(4)
        self.e1.setAlignment(Qt.AlignRight)

        self.e2 = QLineEdit()
        name_validator = QRegExpValidator(QRegExp("[a-zA-Z ]+"))  # Regex to allow alphabets and spaces
        self.e2.setValidator(name_validator)
        self.e2.setMaxLength(30)  # Optional: Set maximum length
        self.e2.setAlignment(Qt.AlignLeft)
        self.e2.setPlaceholderText("Enter name (alphabets and spaces only)")

        self.flo = QFormLayout()
        self.flo.addRow("Total Output", self.e1)
        self.flo.addRow("Checker", self.e2)
        vlayout.addLayout(self.flo)

        self.calender = QCalendarWidget()
        vlayout.addWidget(self.calender)

        self.b1 = QPushButton("Submit")
        self.b1.setCheckable(True)
        self.b1.clicked.connect(self.confirmation)
        vlayout.addWidget(self.b1)

        self.reject_details = {
            "dust_marks", "under_spray", "scratches", "dented", "bubble", "dust_paint", "sink_mark", "black_dot", "white_dot",
            "smear", "dirty", "bulging", "short_mould", "weldline", "incompleted", "colour_out", "gate_high", "over_stamp",
            "ink_mark", "banding", "shining", "overtrim", "dprinting", "dust_fibre", "thiner_mark", "position_out", "adjustment"
        }
        
        self.spin_boxes = {}

        for i, detail in enumerate(self.reject_details):
            label = QLabel(detail.replace('_', ' ').capitalize())
            spin_box = QSpinBox()
            spin_box.setRange(0, 100)
            self.spin_boxes[detail] = spin_box

            grid.addWidget(label, i // 2, (i % 2) * 2)
            grid.addWidget(spin_box, i // 2, (i % 2) * 2 + 1)

        hlayout.addLayout(vlayout)
        hlayout.addLayout(grid)
        self.setLayout(hlayout)

    def clear_defect_details(self):
        # Clear all spin boxes in the reject details
        for spin_box in self.spin_boxes.values():
            spin_box.setValue(0)  # Reset each spin box value to 0

    def confirmation(self):
        part_code = self.part_code
        checked_output_amount = self.e1.text()
        date_checked = self.calender.selectedDate().toString("yyyy-MM-dd")
        checker = self.e2.text().upper()

        # Collect non-zero rejection details
        non_zero_defects = {detail: spin_box.value() for detail, spin_box in self.spin_boxes.items() if spin_box.value() > 0}

        # Format non-zero rejection details for display using HTML for better alignment
        rejection_details_text = "<br>".join([f"{detail.replace('_', ' ').capitalize()}: {value}" for detail, value in non_zero_defects.items()])

        # Set up the confirmation message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Please confirm entered values")
        msg.setInformativeText(
            f"<b>Part Code:</b> {part_code}<br>"
            f"<b>Total Checked:</b> {checked_output_amount}<br>"
            f"<b>Total Rejected:</b> {sum(non_zero_defects.values())}<br>"
            f"<b>Date Checked:</b> {date_checked}<br>"
            f"<b>Checker:</b> {checker}<br><br>"
            f"<b>Rejection Details:</b><br>{rejection_details_text if rejection_details_text else 'None'}"
        )
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # Capture the button clicked and proceed with submission only if OK is clicked
        if msg.exec_() == QMessageBox.Ok:
            self.submit_final_phase_checking()




    def submit_final_phase_checking(self):

         date_print = self.calender.selectedDate().toString("yyyy-MM-dd")
         print_output_amount = self.e1.text()
         defect_data = {}
         total_defects = 0
         checker = self.e2.text().upper()

         try:
            # Start a transaction
            my_cursor.execute("START TRANSACTION;")
            
            # Fetch part_name and parent_id based on the entered part code
            my_cursor.execute(
                  "SELECT part_name, parent_id FROM main_parts WHERE part_code = %s", 
                  (self.part_code,)
            )

            result = my_cursor.fetchone()

            # Collect defect data from spin boxes
            for defect, spin_box in self.spin_boxes.items():
                defect_data[defect] = spin_box.value()
                total_defects += spin_box.value()  # Sum up total defects

            if result:
                  part_name, parent_id = result
            else:
                  print("No matching part found for the given part code.")
                  my_cursor.execute("ROLLBACK;")  # Rollback if no matching part
                  return
            
            sql_print_history = """
            INSERT INTO history_print
            (date_print, part_name, part_code, amount_inspect, amount_reject, parent_id, movement_reason, print_info_id, checker_name, date_entered) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            print_history_inputs = (
            date_print,
            part_name,
            self.part_code,
            print_output_amount,
            total_defects if total_defects is not None else 0,
            parent_id,
            "200",
            self.print_id,
            checker
            )
            my_cursor.execute(sql_print_history, print_history_inputs)

            # Retrieve the new print_inspection_id
            my_cursor.execute("SELECT LAST_INSERT_ID();")
            last_print_inspection_id = my_cursor.fetchone()[0]

            # Insert defects into `print_defect_list` using the correct `print_inspection_id`
            sql_defect_list = """
            INSERT INTO print_defect_list
            (print_inspection_id, dust_mark, under_spray, scratches ,dented ,bubble ,dust_paint, 
            sink_mark ,black_dot ,white_dot ,smear ,dirty ,bulging ,short_mould, 
            weldline ,incompleted ,colour_out ,gate_high ,over_stamp ,ink_mark ,banding, shining,
            overtrim ,dprinting ,dust_fibre ,thiner_mark,position_out, adjustment)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """

            values = (last_print_inspection_id,) + tuple(defect_data.get(defect, 0) for defect in self.reject_details) 
            my_cursor.execute(sql_defect_list, values)

            # Commit to finalize the `print_defect_list` insert
            mydb.commit()
            print("Data Inserted")

            self.e1.clear()  # Clear the total output QLineEdit
            self.e2.clear()  # Clear the total output QLineEdit
            self.calender.setSelectedDate(QDate.currentDate())  # Reset the calendar to today's date
            self.clear_defect_details()


         except mysql.connector.Error as e:
            mydb.rollback()  # Roll back transaction in case of an error
            print(f"Error: {e}")


class to_store(QWidget):
    def __init__(self,  parent=None):
         super(to_store, self).__init__(parent)
   
         hlayout = QHBoxLayout()
      
         self.b1 = QPushButton("Spray")
         self.b1.setChecked(True)
         self.b1.clicked.connect(self.open_to_store_spray)
         hlayout.addWidget(self.b1)
         
         self.b2 = QPushButton("Print")
         self.b2.setChecked(True)
         self.b2.clicked.connect(self.open_to_store_print)
         hlayout.addWidget(self.b2)

         self.setLayout(hlayout)
         self.open_to_store_spray_window = None
         self.open_to_store_print_window = None


      
    def open_to_store_spray (self):
          
        if self.open_to_store_spray_window is None:
            self.open_to_store_spray_window = to_store_spray()
        
        # Show the open_new_batch_print_window window
        self.open_to_store_spray_window.show()

    def open_to_store_print (self):
          
        if self.open_to_store_print_window is None:
            self.open_to_store_print_window = to_store_print()
        
        # Show the open_new_batch_print_window window
        self.open_to_store_print_window.show()

class to_store_spray(QWidget):
    # Define the signal at the class level
    part_selected = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super(to_store_spray, self).__init__(parent)
        self.open_entry_form_instance = None

        # Main vertical layout
        vlayout = QVBoxLayout()
        
        # Horizontal layout for radio buttons
        hlayout = QHBoxLayout()

        # Create radio buttons
        self.r1 = QRadioButton("100 %")
        self.r1.setChecked(True)
        self.r2 = QRadioButton("200 %")
        self.r2.setChecked(False)

        
        # Add radio buttons to horizontal layout
        hlayout.addWidget(self.r1)
        hlayout.addWidget(self.r2)
        
        # Add the horizontal layout with radio buttons to the main layout
        vlayout.addLayout(hlayout)

        # Connect radio buttons to the toggle handler
        self.r1.toggled.connect(self.on_radio_button_toggled)
        self.r2.toggled.connect(self.on_radio_button_toggled)

        # Calendar widget
        self.calender = QCalendarWidget()
        vlayout.addWidget(self.calender)
        self.calender.clicked[QDate].connect(self.load_parts_for_date)

        # List widget
        self.listWidget = QListWidget()
        vlayout.addWidget(self.listWidget)
        self.listWidget.itemClicked.connect(self.on_item_clicked)

        # Label for selected part
        self.selected_part_label = QLabel("Selected Part Name:")
        vlayout.addWidget(self.selected_part_label)

        # Set main layout for the QWidget
        self.setLayout(vlayout)

        # Load initial parts for the selected date
        self.load_parts_for_date(self.calender.selectedDate())
        self.resize(1000, 500)

    def on_radio_button_toggled(self):
        # Refresh the list whenever the radio button selection changes
        self.load_parts_for_date(self.calender.selectedDate())

    def load_parts_for_date(self, selected_date):
        # Clear the list widget to refresh with new data
        self.listWidget.clear()

        # Convert QDate to string in format 'YYYY-MM-DD'
        date_str = selected_date.toString("yyyy-MM-dd")

        # Determine the query based on the selected radio button
        if self.r1.isChecked() == True:
            query = """
                SELECT spray_batch_id, part_code, part_name, hundered_balance 
                FROM spray_batch_info 
                WHERE date_sprayed = %s
            """
        else:
            query = """
                SELECT spray_batch_id, part_code, part_name, finished_goods_balance 
                FROM spray_batch_info 
                WHERE date_sprayed = %s
            """
        
        # Example for executing the query (assuming my_cursor and database connection exist)
        # Replace this with your actual database handling code
        my_cursor.execute(query, (date_str,))
        part_list = my_cursor.fetchall()

        
        # Populate list widget with parts information
        if self.r1.isChecked():
            for spray_batch_id, part_code, part_name, hundered_balance in part_list:
                part_info = f"Spray Batch ID: {spray_batch_id}, Part Name: {part_name}, Part Code: {part_code}, 100% Balance: {hundered_balance}"
                self.listWidget.addItem(part_info)
        else:
            for spray_batch_id, part_code, part_name, finished_goods_balance in part_list:
                part_info = f"Spray Batch ID: {spray_batch_id}, Part Name: {part_name}, Part Code: {part_code}, 200% Balance: {finished_goods_balance}"
                self.listWidget.addItem(part_info)

    def on_item_clicked(self, item):
        # Parse the spray ID and part code from the selected item text
        item_text = item.text()
        spray_id = int(item_text.split(",")[0].split(":")[1].strip())
        part_code = item_text.split(",")[2].split(":")[1].strip()

        # Emit the signal and open the entry form with parsed spray_id and part_code
        self.part_selected.emit(spray_id, part_code)  # Emit the signal

        # Optionally, call open_entry_form
        self.open_entry_form(spray_id, part_code)

    def open_entry_form(self, spray_id, part_code):
        # Check if the window is already open; if not, create it
        if self.open_entry_form_instance is None:
            self.open_entry_form_instance = open_to_store_spray_entry(spray_id, part_code, self)
        
        # Update the part label if the form is already open
        else:
            self.open_entry_form_instance.spray_id = spray_id
            self.open_entry_form_instance.part_code = part_code
            self.open_entry_form_instance.selected_part_label.setText(f"Selected Part Code: {part_code}")

        # Show the window
        self.open_entry_form_instance.show()


    def reset_radio_buttons(self):
        self.r1.setChecked(True)  # Set the first radio button as checked
        self.r2.setChecked(False)  # Set the first radio button as checked

class open_to_store_spray_entry(QWidget):
    def __init__(self, spray_id, part_code,to_store_spray_instance, parent=None):
        super(open_to_store_spray_entry, self).__init__(parent)

        self.spray_id = spray_id
        self.part_code = part_code
        self.to_store_spray_instance = to_store_spray_instance

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        grid = QGridLayout()

        # Output amount
        self.selected_part_label = QLabel(f"Selected Part Code: {part_code}")
        vlayout.addWidget(self.selected_part_label)
        
        self.e1 = QLineEdit()
        self.e1.setValidator(QIntValidator())
        self.e1.setMaxLength(4)
        self.e1.setAlignment(Qt.AlignRight)

        self.flo = QFormLayout()
        self.flo.addRow("Total Send To Store", self.e1)
        vlayout.addLayout(self.flo)

        # Date Printed
        self.calender = QCalendarWidget()
        vlayout.addWidget(self.calender)

        # Submit Button
        self.b1 = QPushButton("Submit")
        self.b1.setCheckable(True)
        self.b1.clicked.connect(self.confirmation)
        vlayout.addWidget(self.b1)

        hlayout.addLayout(vlayout)
        hlayout.addLayout(grid)
        self.setLayout(hlayout)

    def confirmation(self):
        part_code = self.part_code
        checked_output_amount = self.e1.text()
        date_checked = self.calender.selectedDate().toString("yyyy-MM-dd")


        # # Collect non-zero rejection details
        # non_zero_defects = {detail: spin_box.value() for detail, spin_box in self.spin_boxes.items() if spin_box.value() > 0}

        # # Format non-zero rejection details for display using HTML for better alignment
        # rejection_details_text = "<br>".join([f"{detail.replace('_', ' ').capitalize()}: {value}" for detail, value in non_zero_defects.items()])

        # Set up the confirmation message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Please confirm entered values")
        msg.setInformativeText(
            f"<b>Part Code:</b> {part_code}<br>"
            f"<b>Total Send To Store:</b> {checked_output_amount}<br>"
            # f"<b>Total Rejected:</b> {sum(non_zero_defects.values())}<br>"
            f"<b>Date Send To Store:</b> {date_checked}<br>"
            # f"<b>Checker:</b> {checker}<br><br>"
            # f"<b>Rejection Details:</b><br>{rejection_details_text if rejection_details_text else 'None'}"
        )
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # Capture the button clicked and proceed with submission only if OK is clicked
        if msg.exec_() == QMessageBox.Ok:
            self.submit_to_store_spray_check()
      
    def submit_to_store_spray_check(self):

         date_checked = self.calender.selectedDate().toString("yyyy-MM-dd")
         checked_output_amount = self.e1.text()
         defect_data = {}
         total_defects = 0

         try:
            # Start a transaction
            my_cursor.execute("START TRANSACTION;")
            
            # Fetch part_name and parent_id based on the entered part code
            my_cursor.execute(
                  "SELECT part_name, parent_id FROM main_parts WHERE part_code = %s", 
                  (self.part_code,)
            )

            result = my_cursor.fetchone()

            if result:
                  part_name, parent_id = result
            else:
                  print("No matching part found for the given part code.")
                  my_cursor.execute("ROLLBACK;")  # Rollback if no matching part
                  return
            
            # Check if `spray_batch_id` exists in `print_batch_info`
            my_cursor.execute(
                  "SELECT print_info_id FROM print_batch_info WHERE spray_batch_id = %s",
                  (self.spray_id,)
            )
            result = my_cursor.fetchone()

            # Insert into `history_print` table
            sql_spray_history = """
                INSERT INTO history_spray
                (movement_date, part_name, part_code, amount_inspect, amount_reject, parent_id, spray_batch_id, movement_reason, date_entered) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            movement_reason = "pn100" if self.to_store_spray_instance.r1.isChecked() else "pn200"

            spray_history_inputs = (
                date_checked,
                part_name,
                self.part_code,
                checked_output_amount,
                total_defects if total_defects is not None else 0, ### problem here
                parent_id,
                self.spray_id,
                movement_reason
            )

            """
            so here is insert into spray history first
            """
            my_cursor.execute(sql_spray_history, spray_history_inputs)
            # my_cursor.execute("SELECT LAST_INSERT_ID();")
            # last_spray_inspection_id = my_cursor.fetchone()[0]

            # # Insert defects into `print_defect_list` using the correct `print_inspection_id`
            # sql_defect_list = """
            # INSERT INTO spray_defect_list
            # (spray_inspection_id, dust_mark, fibre_mark, paint_marks, white_marks, sink_marks, texture_marks, water_marks,
            # flow_marks, black_dot, white_dot, over_paint, under_spray, colour_out, masking_ng, flying_paint, weldline,
            # banding, short_mould, sliver_streak, dented, scratches, dirty)
            # VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            # """

            # values = (last_spray_inspection_id,) + tuple(defect_data.get(defect, 0) for defect in self.reject_details) 
            # my_cursor.execute(sql_defect_list, values)

            # Commit to finalize the `print_defect_list` insert
            mydb.commit()
            print("Data Inserted")

            # In the other class where you want to call reset_radio_buttons:
            # In the `submit_to_store_spray_check` method
            # self.to_store_spray_instance.reset_radio_buttons()
            self.e1.clear()
            self.calender.setSelectedDate(QDate.currentDate())  # Reset the calendar to today's date

         except mysql.connector.Error as e:
            mydb.rollback()  # Roll back transaction in case of an error
            print(f"Error: {e}")

##______________________________________________________________________________________________________________________________________________________

class to_store_print(QWidget):
    # Define the signal at the class level
    part_selected = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super(to_store_print, self).__init__(parent)
        self.open_entry_form_instance = None
        

        # Main vertical layout
        vlayout = QVBoxLayout()
        
        # Horizontal layout for radio buttons
        hlayout = QHBoxLayout()

        # Create radio buttons
        self.r1 = QRadioButton("100 %")
        self.r1.setChecked(True)
        self.r2 = QRadioButton("200 %")
        self.r2.setChecked(False)

        
        # Add radio buttons to horizontal layout
        hlayout.addWidget(self.r1)
        hlayout.addWidget(self.r2)
        
        # Add the horizontal layout with radio buttons to the main layout
        vlayout.addLayout(hlayout)

        # Connect radio buttons to the toggle handler
        self.r1.toggled.connect(self.on_radio_button_toggled)
        self.r2.toggled.connect(self.on_radio_button_toggled)

        # Calendar widget
        self.calender = QCalendarWidget()
        vlayout.addWidget(self.calender)
        self.calender.clicked[QDate].connect(self.load_parts_for_date)

        # List widget
        self.listWidget = QListWidget()
        vlayout.addWidget(self.listWidget)
        self.listWidget.itemClicked.connect(self.on_item_clicked)

        # Label for selected part
        self.selected_part_label = QLabel("Selected Part Name:")
        vlayout.addWidget(self.selected_part_label)

        # Set main layout for the QWidget
        self.setLayout(vlayout)

        # Load initial parts for the selected date
        self.load_parts_for_date(self.calender.selectedDate())
        self.resize(1000, 500)

    def reset_radio_buttons(self):
        self.r1.setChecked(True)  # Set the first radio button as checked
        self.r2.setChecked(False)  # Set the first radio button as checked

    def on_radio_button_toggled(self):
        # Refresh the list whenever the radio button selection changes
        self.load_parts_for_date(self.calender.selectedDate())

    def load_parts_for_date(self, selected_date):
        # Clear the list widget to refresh with new data
        self.listWidget.clear()

        # Convert QDate to string in format 'YYYY-MM-DD'
        date_str = selected_date.toString("yyyy-MM-dd")

        # Determine the query based on the selected radio button
        if self.r1.isChecked():
            query = """
                SELECT print_info_id, part_code, part_name, hundered_balance 
                FROM print_batch_info 
                WHERE date_printed = %s
            """
        else:
            query = """
                SELECT print_info_id, part_code, part_name, finished_good_balance 
                FROM print_batch_info 
                WHERE date_printed = %s
            """
        
        # Example for executing the query (assuming my_cursor and database connection exist)
        # Replace this with your actual database handling code
        my_cursor.execute(query, (date_str,))
        part_list = my_cursor.fetchall()

        
        # Populate list widget with parts information
        if self.r1.isChecked():
            for print_info_id, part_code, part_name, hundered_balance in part_list:
                part_info = f"Print Batch ID: {print_info_id}, Part Name: {part_name}, Part Code: {part_code}, 100% Balance: {hundered_balance}"
                self.listWidget.addItem(part_info)
        else:
            for print_info_id, part_code, part_name, finished_goods_balance in part_list:
                part_info = f"Print Batch ID: {print_info_id}, Part Name: {part_name}, Part Code: {part_code}, 200% Balance: {finished_goods_balance}"
                self.listWidget.addItem(part_info)

    def on_item_clicked(self, item):
        # Parse the spray ID and part code from the selected item text
        item_text = item.text()
        print_id = int(item_text.split(",")[0].split(":")[1].strip())
        part_code = item_text.split(",")[2].split(":")[1].strip()

        # Emit the signal and open the entry form with parsed spray_id and part_code
        self.part_selected.emit(print_id, part_code)  # Emit the signal

        # Optionally, call open_entry_form
        self.open_entry_form(print_id, part_code)

    def open_entry_form(self, print_id, part_code):
        # Check if the window is already open; if not, create it
        if self.open_entry_form_instance is None:
            self.open_entry_form_instance = open_to_store_print_entry(print_id, part_code, self)
        
        # Update the part label if the form is already open
        else:
            self.open_entry_form_instance.print_id = print_id
            self.open_entry_form_instance.part_code = part_code
            self.open_entry_form_instance.selected_part_label.setText(f"Selected Part Code: {part_code}")

        # Show the window
        self.open_entry_form_instance.show()

class open_to_store_print_entry(QWidget):
    def __init__(self, print_id, part_code,to_store_print_instance, parent=None):
        super(open_to_store_print_entry, self).__init__(parent)

        self.print_id = print_id
        self.part_code = part_code
        self.to_store_print_instance = to_store_print_instance

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        grid = QGridLayout()

        # Output amount
        self.selected_part_label = QLabel(f"Selected Part Code: {part_code}")
        vlayout.addWidget(self.selected_part_label)
        
        self.e1 = QLineEdit()
        self.e1.setValidator(QIntValidator())
        self.e1.setMaxLength(4)
        self.e1.setAlignment(Qt.AlignRight)

        self.flo = QFormLayout()
        self.flo.addRow("Total Send To Store", self.e1)
        vlayout.addLayout(self.flo)

        # Date Printed
        self.calender = QCalendarWidget()
        vlayout.addWidget(self.calender)

        # Submit Button
        self.b1 = QPushButton("Submit")
        self.b1.setCheckable(True)
        self.b1.clicked.connect(self.confirmation)
        vlayout.addWidget(self.b1)

        # Defect details with spin boxes
        # self.reject_details = {
        #     "dust_marks","fibre_marks","paint_marks","white_marks","sink_marks","texture_marks","water_marks",
        #     "flow_marks","black_dot","white_dot","over_paint","under_spray","colour_out","masking_ng","flying_paint","weldline",
        #     "banding","short_mould","sliver_streak","dented","scratches","dirty"
        # }
        # self.spin_boxes = {}

        # # Populate grid with labels and spin boxes
        # for i, detail in enumerate(self.reject_details):
        #     label = QLabel(detail.replace('_', ' ').capitalize())
        #     spin_box = QSpinBox()
        #     spin_box.setRange(0, 100)  # Set range as needed
        #     self.spin_boxes[detail] = spin_box  # Store reference to each spin box

        #     grid.addWidget(label, i // 2, (i % 2) * 2)
        #     grid.addWidget(spin_box, i // 2, (i % 2) * 2 + 1)

        hlayout.addLayout(vlayout)
        hlayout.addLayout(grid)
        self.setLayout(hlayout)

    def confirmation(self):
        part_code = self.part_code
        checked_output_amount = self.e1.text()
        date_checked = self.calender.selectedDate().toString("yyyy-MM-dd")


        # # Collect non-zero rejection details
        # non_zero_defects = {detail: spin_box.value() for detail, spin_box in self.spin_boxes.items() if spin_box.value() > 0}

        # # Format non-zero rejection details for display using HTML for better alignment
        # rejection_details_text = "<br>".join([f"{detail.replace('_', ' ').capitalize()}: {value}" for detail, value in non_zero_defects.items()])

        # Set up the confirmation message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Please confirm entered values")
        msg.setInformativeText(
            f"<b>Part Code:</b> {part_code}<br>"
            f"<b>Total Send To Store:</b> {checked_output_amount}<br>"
            # f"<b>Total Rejected:</b> {sum(non_zero_defects.values())}<br>"
            f"<b>Date Send To Store:</b> {date_checked}<br>"
            # f"<b>Checker:</b> {checker}<br><br>"
            # f"<b>Rejection Details:</b><br>{rejection_details_text if rejection_details_text else 'None'}"
        )
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # Capture the button clicked and proceed with submission only if OK is clicked
        if msg.exec_() == QMessageBox.Ok:
            self.submit_to_store_print_check()
      
    def submit_to_store_print_check(self):

         date_checked = self.calender.selectedDate().toString("yyyy-MM-dd")
         checked_output_amount = self.e1.text()
         defect_data = {}
         total_defects = 0

         try:
            # Start a transaction
            my_cursor.execute("START TRANSACTION;")
            
            # Fetch part_name and parent_id based on the entered part code
            my_cursor.execute(
                  "SELECT part_name, parent_id FROM main_parts WHERE part_code = %s", 
                  (self.part_code,)
            )

            result = my_cursor.fetchone()

            if result:
                  part_name, parent_id = result
            else:
                  print("No matching part found for the given part code.")
                  my_cursor.execute("ROLLBACK;")  # Rollback if no matching part
                  return
            
            # Check if `spray_batch_id` exists in `print_batch_info`
            my_cursor.execute(
                  "SELECT print_info_id FROM print_batch_info WHERE spray_batch_id = %s",
                  (self.print_id,)
            )
            result = my_cursor.fetchone()

            # Insert into `history_print` table
            sql_print_history = """
                INSERT INTO history_print
                (date_print, part_name, part_code, amount_inspect, amount_reject, parent_id, print_info_id, movement_reason, date_entered ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,CURRENT_TIMESTAMP)
            """
            movement_reason = "pn100" if self.to_store_print_instance.r1.isChecked() else "pn200"

            print_history_inputs = (
                date_checked,
                part_name,
                self.part_code,
                checked_output_amount,
                total_defects if total_defects is not None else 0, ### problem here
                parent_id,
                self.print_id,
                movement_reason
            )

            """
            so here is insert into spray history first
            """
            my_cursor.execute(sql_print_history, print_history_inputs)
            # my_cursor.execute("SELECT LAST_INSERT_ID();")
            # last_print_inspection_id = my_cursor.fetchone()[0]

            # # Insert defects into `print_defect_list` using the correct `print_inspection_id`
            # sql_defect_list = """
            # INSERT INTO print_defect_list
            # (print_inspection_id, dust_mark, under_spray, scratches, dented, bubble, dust_paint, 
            # sink_mark, black_dot, white_dot, smear, dirty, bulging, short_mould, 
            # weldline, incompleted, colour_out, gate_high, over_stamp, ink_mark, banding, shining,
            # overtrim, dprinting, dust_fibre, thiner_mark)
            # VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            # """

            # values = (last_print_inspection_id,) + tuple(defect_data.get(defect, 0) for defect in self.reject_details) 
            # my_cursor.execute(sql_defect_list, values)

            # Commit to finalize the `print_defect_list` insert
            mydb.commit()
            print("Data Inserted")

            # In the other class where you want to call reset_radio_buttons:
            # In the `submit_to_store_spray_check` method
            # self.to_store_spray_instance.reset_radio_buttons()
            self.e1.clear()
            self.calender.setSelectedDate(QDate.currentDate())  # Reset the calendar to today's date

         except mysql.connector.Error as e:
            mydb.rollback()  # Roll back transaction in case of an error
            print(f"Error: {e}")
    

class rework_checking(QWidget):

    part_selected = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super(rework_checking, self).__init__(parent)
        self.resize(1000, 500)

        vlayout = QVBoxLayout()

        self.calender = QCalendarWidget()
        vlayout.addWidget(self.calender)
        self.calender.clicked[QDate].connect(self.load_parts_for_date)

        self.listWidget = QListWidget()
        vlayout.addWidget(self.listWidget)
        # Connect the itemClicked signal to the on_item_clicked function
        self.listWidget.itemClicked.connect(self.on_item_clicked)

        self.selected_part_label = QLabel("Selected Part Name:")
        vlayout.addWidget(self.selected_part_label)

        self.setLayout(vlayout)

        self.load_parts_for_date(self.calender.selectedDate())
        self.open_entry_form_instance = None  # Renamed to avoid conflict with method name

    def load_parts_for_date(self, selected_date):
        # Clear the list widget to refresh with new data
        self.listWidget.clear()

        # Convert QDate to string in format 'YYYY-MM-DD'
        date_str = selected_date.toString("yyyy-MM-dd")

        # Fetch data for the selected date
        query = """
            SELECT spray_batch_id, part_code, part_name, recheck_balance 
            FROM spray_batch_info 
            WHERE date_sprayed = %s
        """
        my_cursor.execute(query, (date_str,))
        part_list = my_cursor.fetchall()

        # Populate list widget with parts information
        for spray_batch_id, part_code, part_name, recheck_balance in part_list:
            # Use total_output as unchecked_balance if unchecked_balance is None
            display_balance = recheck_balance
            part_info = f"Spray Batch ID: {spray_batch_id}, Part Name: {part_name}, Part Code: {part_code}, Recheck Balance: {display_balance}"
            self.listWidget.addItem(part_info)


    def on_item_clicked(self, item):
         # Parse the spray ID and part code from the selected item text
         item_text = item.text()
         spray_id = item_text.split(",")[0].split(":")[1].strip()
         part_code = item_text.split(",")[2].split(":")[1].strip()

         # Emit the signal and open the entry form with parsed spray_id and part_code
         self.part_selected.emit(int(spray_id), part_code)  # Emit the signal

         # Optionally, call open_entry_form
         self.open_entry_form(spray_id, part_code)

    def open_entry_form(self, spray_id, part_code):
         # Check if the window is already open; if not, create it
         if self.open_entry_form_instance is None:
               self.open_entry_form_instance = open_rechecking_entry(spray_id, part_code)
         
         # Update the part label if the form is already open
         else:
               self.open_entry_form_instance.spray_id = spray_id
               self.open_entry_form_instance.part_code = part_code
               self.open_entry_form_instance.selected_part_label.setText(f"Selected Part Code: {part_code}")

         # Show the window
         self.open_entry_form_instance.show()

class open_rechecking_entry(QWidget):
      def __init__(self, spray_id, part_code, parent=None):
         super(open_rechecking_entry, self).__init__(parent)

         self.spray_id = spray_id
         self.part_code = part_code

         vlayout = QVBoxLayout()
         hlayout = QHBoxLayout()
         grid = QGridLayout()

         # Output amount
         self.selected_part_label = QLabel(f"Selected Part Code: {part_code}")
         vlayout.addWidget(self.selected_part_label)
         
         self.e1 = QLineEdit()
         self.e1.setValidator(QIntValidator())
         self.e1.setMaxLength(4)
         self.e1.setAlignment(Qt.AlignRight)

         self.e2 = QLineEdit()
         name_validator = QRegExpValidator(QRegExp("[a-zA-Z ]+"))  # Regex to allow alphabets and spaces
         self.e2.setValidator(name_validator)
         self.e2.setMaxLength(30)  # Optional: Set maximum length
         self.e2.setAlignment(Qt.AlignLeft)
         self.e2.setPlaceholderText("Enter name (alphabets and spaces only)")

         self.flo = QFormLayout()
         self.flo.addRow("Total Checked", self.e1)
         self.flo.addRow("Checker", self.e2)
         vlayout.addLayout(self.flo)

         # Date Printed
         self.calender = QCalendarWidget()
         vlayout.addWidget(self.calender)

         # Submit Button
         self.b1 = QPushButton("Submit")
         self.b1.setCheckable(True)
         self.b1.clicked.connect(self.confirmation)
         vlayout.addWidget(self.b1)

         # Defect details with spin boxes
         self.reject_details = {
                "dust_marks","fibre_marks","paint_marks","white_marks","sink_marks","texture_marks","water_marks",
                "flow_marks","black_dot","white_dot","over_paint","under_spray","colour_out","masking_ng","flying_paint","weldline",
                "banding","short_mould","sliver_streak","dented","scratches","dirty"
            }
         self.spin_boxes = {}

         # Populate grid with labels and spin boxes
         for i, detail in enumerate(self.reject_details):
               label = QLabel(detail.replace('_', ' ').capitalize())
               spin_box = QSpinBox()
               spin_box.setRange(0, 100)  # Set range as needed
               self.spin_boxes[detail] = spin_box  # Store reference to each spin box

               grid.addWidget(label, i // 2, (i % 2) * 2)
               grid.addWidget(spin_box, i // 2, (i % 2) * 2 + 1)

         hlayout.addLayout(vlayout)
         hlayout.addLayout(grid)
         self.setLayout(hlayout)

      def confirmation(self):
        part_code = self.part_code
        checked_output_amount = self.e1.text()
        date_checked = self.calender.selectedDate().toString("yyyy-MM-dd")
        checker = self.e2.text().upper()

        # Collect non-zero rejection details
        non_zero_defects = {detail: spin_box.value() for detail, spin_box in self.spin_boxes.items() if spin_box.value() > 0}

        # Format non-zero rejection details for display using HTML for better alignment
        rejection_details_text = "<br>".join([f"{detail.replace('_', ' ').capitalize()}: {value}" for detail, value in non_zero_defects.items()])

        # Set up the confirmation message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Please confirm entered values")
        msg.setInformativeText(
            f"<b>Part Code:</b> {part_code}<br>"
            f"<b>Total Checked:</b> {checked_output_amount}<br>"
            f"<b>Total Rejected:</b> {sum(non_zero_defects.values())}<br>"
            f"<b>Date Checked:</b> {date_checked}<br>"
            f"<b>Checker:</b> {checker}<br><br>"
            f"<b>Rejection Details:</b><br>{rejection_details_text if rejection_details_text else 'None'}"
        )
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # Capture the button clicked and proceed with submission only if OK is clicked
        if msg.exec_() == QMessageBox.Ok:
            self.submit_first_phase_check()

      def clear_defect_details(self):
        # Clear all spin boxes in the reject details
        for spin_box in self.spin_boxes.values():
         spin_box.setValue(0)  # Reset each spin box value to 0

      
      def submit_first_phase_check(self):
        date_checked = self.calender.selectedDate().toString("yyyy-MM-dd")
        checked_output_amount = self.e1.text()
        defect_data = {}
        total_defects = 0
        checker = self.e2.text().upper()

        try:
            # Start a transaction
            my_cursor.execute("START TRANSACTION;")
            
            # Fetch part_name and parent_id based on the entered part code
            my_cursor.execute(
                "SELECT part_name, parent_id FROM main_parts WHERE part_code = %s", 
                (self.part_code,)
            )
            result = my_cursor.fetchone()
            if result:
                part_name, parent_id = result
            else:
                print("No matching part found for the given part code.")
                my_cursor.execute("ROLLBACK;")  # Rollback if no matching part
                return

            # Check if `spray_batch_id` exists in `print_batch_info`
            my_cursor.execute(
                "SELECT print_info_id FROM print_batch_info WHERE spray_batch_id = %s",
                (self.spray_id,)
            )
            result = my_cursor.fetchone()

            # Collect defect data from spin boxes
            for defect, spin_box in self.spin_boxes.items():
                defect_data[defect] = spin_box.value()
                total_defects += spin_box.value()  # Sum up total defects

            # Insert into `history_spray` table
            sql_spray_history = """
                INSERT INTO history_spray
                (movement_date, part_name, part_code, amount_inspect, amount_reject, parent_id, spray_batch_id, movement_reason, checker_name, date_entered ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            spray_history_inputs = (
                date_checked,
                part_name,
                self.part_code,
                checked_output_amount,
                total_defects,  # Use calculated total defects
                parent_id,
                self.spray_id,
                "rework",
                checker
            )
            my_cursor.execute(sql_spray_history, spray_history_inputs)
            my_cursor.execute("SELECT LAST_INSERT_ID();")
            last_spray_inspection_id = my_cursor.fetchone()[0]

            # Insert defects into `spray_defect_list` using the correct `spray_inspection_id`
            sql_defect_list = """
            INSERT INTO spray_defect_list
            (spray_inspection_id, dust_mark, fibre_mark, paint_marks, white_marks, sink_marks, texture_marks, water_marks,
            flow_marks, black_dot, white_dot, over_paint, under_spray, colour_out, masking_ng, flying_paint, weldline,
            banding, short_mould, sliver_streak, dented, scratches, dirty)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (last_spray_inspection_id,) + tuple(defect_data.get(defect, 0) for defect in self.reject_details)
            my_cursor.execute(sql_defect_list, values)

            # Commit to finalize the `spray_defect_list` insert
            mydb.commit()
            print("Data Inserted")

            self.e1.clear()  # Clear the total output QLineEdit
            self.e2.clear()  # Clear the total output QLineEdit
            self.calender.setSelectedDate(QDate.currentDate())  # Reset the calendar to today's date
            self.clear_defect_details()

        except mysql.connector.Error as e:
            mydb.rollback()  # Roll back transaction in case of an error
            print(f"Error: {e}")


def main():
   app = QApplication([])
   ex = main_menu()
   ex.show()
   sys.exit(app.exec_())
if __name__ == '__main__':
   main()


#    def selected_date(self):
#       selected_date = self.calender.selectedDate().toString("yyyy-MM-dd")
#       self.window2 = new_batch_entry(selected_date)
#       self.window2.show()



