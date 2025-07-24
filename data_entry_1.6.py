import sys
import mysql.connector
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from collections import namedtuple

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="UL1131",
    database="production"
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
      v1 = QVBoxLayout()
      v2 = QVBoxLayout()
      v3 = QVBoxLayout()
      v4 = QVBoxLayout()
      self.resize(200,50)
      self.setWindowTitle("Main Menu")

      self.b1 = QPushButton("New Batch")
      self.b1.setCheckable(True)
      self.b1.clicked.connect(self.open_spray_print_window)
      v1.addWidget(self.b1)

      self.b8 = QPushButton("Assembly")
      self.b8.setCheckable(True)
      self.b8.clicked.connect(self.open_assembly_menu)
      v1.addWidget(self.b8)

      self.b2 = QPushButton("100 % Spray")
      self.b2.setCheckable(True)
      self.b2.clicked.connect(self.open_first_phase_checking_window)
      v2.addWidget(self.b2)

      self.b3 = QPushButton("100 % Print")
      self.b3.setCheckable(True)
      self.b3.clicked.connect(self.open_first_phase_print_checking_window)
      v2.addWidget(self.b3)

      self.b10 = QPushButton("100 % Assembly")
      self.b10.setCheckable(True)
      self.b10.clicked.connect(self.open_first_phase_assembly_checking_window)
      v2.addWidget(self.b10)

      self.b4 = QPushButton("200 %")
      self.b4.setCheckable(True)
      self.b4.clicked.connect(self.open_finished_goods_checking_window)
      v2.addWidget(self.b4)

      self.b4 = QPushButton("To Store")
      self.b4.setCheckable(True)
      self.b4.clicked.connect(self.open_to_store_window)
      v3.addWidget(self.b4)

      self.b9 = QPushButton("QC On Hold")
      self.b9.setCheckable(True)
      self.b9.clicked.connect(self.open_on_hold_menu)
      v3.addWidget(self.b9)

      self.b5 = QPushButton("Rework")
      self.b5.setCheckable(True)
      self.b5.clicked.connect(self.open_rework_window)
      v3.addWidget(self.b5)

      self.b6 = QPushButton("New Parts")
      self.b6.setCheckable(True)
      self.b6.clicked.connect(self.open_new_part_window)
      v4.addWidget(self.b6)

      self.b7 = QPushButton("Delete/Amend")
      self.b7.setCheckable(True)
      self.b7.clicked.connect(self.open_delete_window)
      v4.addWidget(self.b7)

      layout.addLayout(v1)
      layout.addLayout(v2)
      layout.addLayout(v3)
      layout.addLayout(v4)

    
    

      self.setLayout(layout)

      self.spray_print_window = None
      self.first_phase_window = None
      self.finished_goods_checking_window = None
      self.to_store_window = None
      self.rework_window = None
      self.first_phase_print_window = None
      self.first_phase_assembly_window = None
      self.new_part_window = None
      self.amend = None
      self.delete = None
      self.assembly = None
      self.onhold = None
   
   def open_new_part_window(self):
        # Check if the spray_print window is already open; if not, create it
        if self.new_part_window is None:
            self.new_part_window = new_part_window(self.part_codes)
        
        # Show the spray_print window
        self.new_part_window.show()

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

   def open_first_phase_assembly_checking_window(self):
        # Check if the spray_print window is already open; if not, create it
        if self.first_phase_assembly_window is None:
            self.first_phase_assembly_window = first_phase_checking_assembly()
        
        # Show the spray_print window
        self.first_phase_assembly_window.show()
 
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

   def open_amend_window(self):
        # Check if the spray_print window is already open; if not, create it
        if self.amend is None:
            self.amend = amend()
        
        # Show the spray_print window
        self.amend.show()

   def open_delete_window(self):
        # Check if the spray_print window is already open; if not, create it
        if self.delete is None:
            self.delete = delete_record()
        
        # Show the spray_print window
        self.delete.show()

   def open_assembly_menu(self):
        # Check if the spray_print window is already open; if not, create it
        if self.assembly is None:
            self.assembly = assembly_window(self.part_codes)
        
        # Show the spray_print window
        self.assembly.show()    

   def open_on_hold_menu(self):
        # Check if the spray_print window is already open; if not, create it
        if self.onhold is None:
            self.onhold = QCOnHold()
        
        # Show the spray_print window
        self.onhold.show()    
       
        
class amend(QWidget):
    def __init__(self, part_codes, parent = None):
        super(amend, self).__init__(parent)

class new_part_window(QWidget):
    def __init__(self, part_codes, parent = None):
        super(new_part_window, self).__init__(parent)

        layout = QVBoxLayout()
        # Part name
        self.e1 = QLineEdit()
        self.e1.setMaxLength(30)
        self.e1.setAlignment(Qt.AlignRight)

        # Part code
        self.e2 = QLineEdit()
        self.e2.setMaxLength(30)
        self.e2.setAlignment(Qt.AlignRight)
        
        # Customer
        self.e3 = QLineEdit()
        self.e3.setMaxLength(30)
        self.e3.setAlignment(Qt.AlignRight)

        self.flo = QFormLayout()
        self.flo.addRow("Part Name", self.e1)
        self.flo.addRow("Part Code", self.e2)
        self.flo.addRow("Customer", self.e3)
        layout.addLayout(self.flo)

        self.b1 = QPushButton("Submit")
        self.b1.setCheckable(True)
        self.b1.clicked.connect(self.confirmation)
        layout.addWidget(self.b1)

        self.setLayout(layout)

    def confirmation(self):
       
       part_name = self.e1.text().upper()
       part_code = self.e2.text().upper()
       customer  = self.e3.text().upper()

       msg = QMessageBox()
       msg.setIcon(QMessageBox.Information)
       msg.setText("Please confirm entered values")
       msg.setInformativeText(f"""
        Part Name: {part_name}
        Part Code: {part_code}
        Customer: {customer}
         """)
       
       msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
       msg.buttonClicked.connect(self.submit_new_part)
       retval = msg.exec_()

    def submit_new_part(self):
        part_name = self.e1.text().upper()
        part_code = self.e2.text().upper()
        customer  = self.e3.text().upper()

        try:
         # Start a transaction
         my_cursor.execute("START TRANSACTION;")

         sql = """
               INSERT INTO main_parts 
               (part_name, part_code, customer) 
               VALUES (%s, %s, %s)
         """
         values = (part_name, part_code, customer)
         my_cursor.execute(sql, values)

         mydb.commit()  # Commit the changes to the database
         print("Record inserted successfully.")

         self.e1.clear()  # Clear the total output QLineEdit
         self.e2.clear()  # Clear the total reject QLineEdit
         print("Inputs cleared after submission.")

        except Exception as e:
            # Rollback the transaction on error
            my_cursor.execute("ROLLBACK;")
            print(f"Error: {e}")
    


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

      #Output amount
      self.e1 = QLineEdit()
      self.e1.setValidator(QIntValidator())
      self.e1.setMaxLength(5)
      self.e1.setAlignment(Qt.AlignRight)

      #Reject amount
      self.e2 = QLineEdit()
      self.e2.setValidator(QIntValidator())
      self.e2.setMaxLength(3)
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
        self.e1.setMaxLength(5)
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
        "dust_marks", "dust_fibre", "black_dot", "dust_paint", "thiner_mark","incompleted", "banding", "ink_mark","under_spray",
        "shining", "position_out", "smear",   "adjustment",   "scratches", "dirty", "dprinting",  "white_dot", "dented", "bubble",  
        "sink_mark", "bulging", "short_mould", "weldline",  "colour_out", "gate_high", "over_stamp", "overtrim"
        ]

        self.spin_boxes = {}

        # Populate grid with labels and line edits
        for i, detail in enumerate(self.reject_details):
            label = QLabel(detail.replace('_', ' ').capitalize())
            spin_box = QSpinBox()
            spin_box.setRange(0, 5000)  # Set range as needed
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
            INSERT INTO print_defect_list
            (print_inspection_id, dust_mark, dust_fibre, black_dot, dust_paint, thiner_mark, incompleted, banding, ink_mark, under_spray,
            shining, position_out, smear,   adjustment,   scratches, dirty, dprinting,  white_dot, dented, bubble,  
            sink_mark, bulging, short_mould, weldline,  colour_out, gate_high, over_stamp, overtrim)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
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

        # my_cursor.execute("SELECT part_name, part_code FROM main_parts")
        # all_parts_info = my_cursor.fetchall()
        # parts_tuple = namedtuple("parts_info", ["part_name", "part_code"])
        # #part will become part in all_parts, then inputs into parts_info for namedtuple * to unzip the tuple that is pass through 
        # parts = [parts_tuple(*part) for part in all_parts_info]
        # self.part_codes = [part.part_code for part in parts]  

        my_cursor.execute("SELECT part_name, part_code FROM main_parts")
        all_parts_variant_info = my_cursor.fetchall()
        parts_tuple_variant = namedtuple("parts_info", ["part_name", "part_code"])
        # Create a list of named tuples for the parts
        parts_variant = [parts_tuple_variant(*part) for part in all_parts_variant_info]
        self.parts_variant = [part.part_code for part in parts_variant]  # Fix here

        self.spray_id = spray_id
        self.part_code = part_code

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        grid = QGridLayout()

        # Output amount
        self.selected_part_label = QLabel(f"Selected Part Code: {part_code}")
        vlayout.addWidget(self.selected_part_label)

        self.part_code_entry = ExtendedComboBox()
        self.part_code_entry.addItems(self.parts_variant)  # Use corrected attribute
        vlayout.addWidget(self.part_code_entry)
        
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
        # self.reject_details = {
        #     "dust_marks", "under_spray", "scratches", "dented", "bubble", "dust_paint", "sink_mark", "black_dot", "white_dot",
        #     "smear", "dirty", "bulging", "short_mould", "weldline", "incompleted", "colour_out", "gate_high", "over_stamp",
        #     "ink_mark", "banding", "shining", "overtrim", "dprinting", "dust_fibre", "thiner_mark", "position_out", "adjustment"
        # }

        self.reject_details = [
            "dust_marks", "dust_fibre", "black_dot", "dust_paint", "thiner_mark", "incompleted", 
            "banding", "ink_mark", "under_spray", "shining", "position_out", "smear", "adjustment", 
            "scratches", "dirty", "dprinting", "white_dot", "dented", "bubble", "sink_mark", 
            "bulging", "short_mould", "weldline", "colour_out", "gate_high", "over_stamp", "overtrim"
        ]

        self.spin_boxes = {}

         # Populate grid with labels and spin boxes
        for i, detail in enumerate(self.reject_details):
            label = QLabel(detail.replace('_', ' ').capitalize())
            spin_box = QSpinBox()
            spin_box.setRange(0, 5000)  # Set range as needed
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
        variant_part = self.part_code_entry.currentText()

        # Collect non-zero rejection details
        non_zero_defects = {detail: spin_box.value() for detail, spin_box in self.spin_boxes.items() if spin_box.value() > 0}

        # Format non-zero rejection details for display using HTML for better alignment
        rejection_details_text = "<br>".join([f"{detail.replace('_', ' ').capitalize()}: {value}" for detail, value in non_zero_defects.items()])

        # Set up the confirmation message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Please confirm entered values")
        msg.setInformativeText(
            f"<b>Part Code:</b> {variant_part}<br>"
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
      variant_part = self.part_code_entry.currentText()
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
                "SELECT print_info_id, part_code FROM print_batch_info WHERE spray_batch_id = %s",
                (self.spray_id,)
            )
         result = my_cursor.fetchone()



        #  if result:
        #         # If batch exists, use the existing print_info_id
        #         last_print_info_id = result[0]
        #         print("Batch exists, using existing print_info_id:", last_print_info_id)
         if result:
            last_print_info_id, existing_part_code = result  # Unpack values
            print("Batch exists, checking part_code...")

            my_cursor.fetchall()  # Clears any unread results

            if existing_part_code == variant_part:
                print("✅ Part code matches, using existing print_info_id:", last_print_info_id)
            else:
                print("⚠️ Part code mismatch, inserting a new row...")

                # 🛠 Fix: Fetch any unread results to clear the cursor
                my_cursor.fetchall()  # ✅ Ensures all rows are read before INSERT

                sql_print_batch_info = """
                INSERT INTO print_batch_info 
                (part_name, part_code, parent_id, spray_batch_id, date_printed, batch_status)
                VALUES (%s, %s, %s, %s, %s, %s)
                """

                print_batch_input = (
                    part_name,
                    variant_part,
                    parent_id,
                    self.spray_id,
                    date_print,
                    "incomplete"
                )

                my_cursor.execute(sql_print_batch_info, print_batch_input)
                last_print_info_id = my_cursor.lastrowid  # ✅ Get new print_info_id

                print("✅ New print_info_id created:", last_print_info_id)

         else:
            print("🚀 No existing batch, inserting a new row...")

            sql_print_batch_info = """
            INSERT INTO print_batch_info 
            (part_name, part_code, parent_id, spray_batch_id, date_printed, batch_status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            print_batch_input = (
                part_name,
                variant_part,
                parent_id,
                self.spray_id,
                date_print,
                "incomplete"
            )

            my_cursor.execute(sql_print_batch_info, print_batch_input)
            last_print_info_id = my_cursor.lastrowid  # ✅ Get new print_info_id

            print("✅ Inserted new row into print_batch_info with print_info_id:", last_print_info_id)

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
                variant_part,
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
                variant_part,
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
         variant_part,
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
            (print_inspection_id, dust_mark, dust_fibre, black_dot, dust_paint, thiner_mark, incompleted, banding, ink_mark, under_spray,
            shining, position_out, smear,   adjustment,   scratches, dirty, dprinting,  white_dot, dented, bubble,  
            sink_mark, bulging, short_mould, weldline,  colour_out, gate_high, over_stamp, overtrim)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
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
         self.e1.setMaxLength(5)
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
         self.reject_details = [
                "dust_marks","fibre_marks","paint_marks","white_marks","sink_marks","texture_marks","water_marks",
                "flow_marks","black_dot","white_dot","over_paint","under_spray","colour_out","masking_ng","flying_paint","weldline",
                "banding","short_mould","sliver_streak","dented","scratches","dirty"
         ]
         self.spin_boxes = {}

         # Populate grid with labels and spin boxes
         for i, detail in enumerate(self.reject_details):
               label = QLabel(detail.replace('_', ' ').capitalize())
               spin_box = QSpinBox()
               spin_box.setRange(0, 5000)  # Set range as needed
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
        super(first_phase_checking_print,  self).__init__(parent)
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
         self.e1.setMaxLength(5)
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
         self.reject_details = [
    "dust_marks", "dust_fibre", "black_dot", "dust_paint", "thiner_mark", "incompleted", 
    "banding", "ink_mark", "under_spray", "shining", "position_out", "smear", "adjustment", 
    "scratches", "dirty", "dprinting", "white_dot", "dented", "bubble", "sink_mark", 
    "bulging", "short_mould", "weldline", "colour_out", "gate_high", "over_stamp", "overtrim"
        ]

         self.spin_boxes = {}

         # Populate grid with labels and spin boxes
         for i, detail in enumerate(self.reject_details):
            label = QLabel(detail.replace('_', ' ').capitalize())
            spin_box = QSpinBox()
            spin_box.setRange(0, 5000)  # Set range as needed
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
            (print_inspection_id, dust_mark, dust_fibre, black_dot, dust_paint, thiner_mark, incompleted, banding, ink_mark, under_spray,
            shining, position_out, smear,   adjustment,   scratches, dirty, dprinting,  white_dot, dented, bubble,  
            sink_mark, bulging, short_mould, weldline,  colour_out, gate_high, over_stamp, overtrim)
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

#############################################################################################################################################




class first_phase_checking_assembly(QWidget):

    part_selected = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super(first_phase_checking_assembly,  self).__init__(parent)
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
            SELECT assembly_info_id, part_code, part_name, secondary_process_balance, total_output
            FROM assembly_batch_info 
            WHERE date_assemble = %s
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
               self.open_entry_form_instance = open_first_phase_checking_assembly_entry(print_id, part_code)
         
         # Update the part label if the form is already open
         else:
               self.open_entry_form_instance.print_id = print_id
               self.open_entry_form_instance.part_code = part_code
               self.open_entry_form_instance.selected_part_label.setText(f"Selected Part Code: {part_code}")

         # Show the window
         self.open_entry_form_instance.show()

class open_first_phase_checking_assembly_entry(QWidget):
      def __init__(self, print_id, part_code, parent=None):
         super(open_first_phase_checking_assembly_entry, self).__init__(parent)

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
         self.e1.setMaxLength(5)
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
         self.reject_details = [
        "missing_components", "dented", "scratches", "sliver_streak", "ink_mark","incompleted", "dirty", "dust","fibre",
        "extra_screw", "extra_nanowl", "light_bubble"
        ]

         self.spin_boxes = {}

         # Populate grid with labels and spin boxes
         for i, detail in enumerate(self.reject_details):
            label = QLabel(detail.replace('_', ' ').capitalize())
            spin_box = QSpinBox()
            spin_box.setRange(0, 5000)  # Set range as needed
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
            sql_assemble_history = """
                INSERT INTO history_assembly
                (date_assemble, part_name, part_code, amount_inspect, amount_reject, parent_id, assembly_info_id, movement_reason, checker_name, date_entered) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """

            assemble_history_inputs = (
                date_checked,
                part_name,
                self.part_code,
                checked_output_amount,
                total_defects if total_defects is not None else 0,  # Use calculated total defects
                parent_id,
                self.print_id,
                "100",
                checker
            )
            my_cursor.execute(sql_assemble_history, assemble_history_inputs)
            my_cursor.execute("SELECT LAST_INSERT_ID();")
            last_print_inspection_id = my_cursor.fetchone()[0]

            # Insert defects into `print_defect_list` using the correct `spray_inspection_id`
            sql_defect_list = """
            INSERT INTO assembly_defect_list
            (assembly_inspection_id,missing_components, dented, scratches, sliver_streak, ink_mark,incompleted, dirty, dust,fibre,
            extra_screw, extra_nanowl, light_bubble)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
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




###########################################################################################################################################################

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

         self.b3 = QPushButton("Assembly")
         self.b3.setChecked(True)
         self.b3.clicked.connect(self.open_finished_goods_assembly)
         hlayout.addWidget(self.b3)

         self.setLayout(hlayout)
         self.open_finished_goods_spray_window = None
         self.open_finished_goods_print_window = None
         self.open_finished_goods_assembly_window = None
      
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

      def open_finished_goods_assembly (self):
          
        if self.open_finished_goods_assembly_window is None:
            self.open_finished_goods_assembly_window = finished_goods_assembly()
        
        # Show the open_new_batch_print_window window
        self.open_finished_goods_assembly_window.show()

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
         self.e1.setMaxLength(5)
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
         self.reject_details = [
                "dust_marks","fibre_marks","paint_marks","white_marks","sink_marks","texture_marks","water_marks",
                "flow_marks","black_dot","white_dot","over_paint","under_spray","colour_out","masking_ng","flying_paint","weldline",
                "banding","short_mould","sliver_streak","dented","scratches","dirty"
         ]
         self.spin_boxes = {}

         # Populate grid with labels and spin boxes
         for i, detail in enumerate(self.reject_details):
               label = QLabel(detail.replace('_', ' ').capitalize())
               spin_box = QSpinBox()
               spin_box.setRange(0, 5000)  # Set range as needed
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
        self.e1.setMaxLength(5)
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

        self.reject_details = [
        "dust_marks", "dust_fibre", "black_dot", "dust_paint", "thiner_mark", "incompleted", 
        "banding", "ink_mark", "under_spray", "shining", "position_out", "smear", "adjustment", 
        "scratches", "dirty", "dprinting", "white_dot", "dented", "bubble", "sink_mark", 
        "bulging", "short_mould", "weldline", "colour_out", "gate_high", "over_stamp", "overtrim"
    ]

        self.spin_boxes = {}

         # Populate grid with labels and spin boxes
        for i, detail in enumerate(self.reject_details):
            label = QLabel(detail.replace('_', ' ').capitalize())
            spin_box = QSpinBox()
            spin_box.setRange(0, 5000)  # Set range as needed
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
            (print_inspection_id, dust_mark, dust_fibre, black_dot, dust_paint, thiner_mark, incompleted, banding, ink_mark, under_spray,
            shining, position_out, smear,   adjustment,   scratches, dirty, dprinting,  white_dot, dented, bubble,  
            sink_mark, bulging, short_mould, weldline,  colour_out, gate_high, over_stamp, overtrim)
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


class finished_goods_assembly(QWidget):
    part_selected = pyqtSignal(int, str)  # Move signal outside __init__

    def __init__(self, parent=None):
        super(finished_goods_assembly, self).__init__(parent)

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
            SELECT assembly_info_id, part_code, part_name, hundered_balance 
            FROM assembly_batch_info 
            WHERE date_assemble = %s
        """
        my_cursor.execute(query, (date_str,))
        part_list = my_cursor.fetchall()

        for assemble_info_id, part_code, part_name, hundered_balance in part_list:
            part_info = f"Assemble Batch ID: {assemble_info_id}, Part Name: {part_name}, Part Code: {part_code}, 100% Balance: {hundered_balance}"
            self.listWidget.addItem(part_info)

    def on_item_clicked(self, item):
        item_text = item.text()
        assemble_id = int(item_text.split(",")[0].split(":")[1].strip())
        part_code = item_text.split(",")[2].split(":")[1].strip()

        self.part_selected.emit(assemble_id, part_code)  # Emit the signal
        self.open_entry_form(assemble_id, part_code)

    def open_entry_form(self, assemble_id, part_code):
        if self.open_entry_form_instance is None:
            self.open_entry_form_instance = open_final_phase_checking_entry(assemble_id, part_code)
        else:
            self.open_entry_form_instance.assemble_id = assemble_id
            self.open_entry_form_instance.part_code = part_code
            self.open_entry_form_instance.selected_part_label.setText(f"Selected Part Code: {part_code}")
        
        self.open_entry_form_instance.show()


class open_final_phase_checking_entry(QWidget):
    def __init__(self, assemble_id, part_code, parent=None):
        super(open_final_phase_checking_entry, self).__init__(parent)  # Use correct class name

        self.assemble_id = assemble_id
        self.part_code = part_code

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        grid = QGridLayout()

        self.selected_part_label = QLabel(f"Selected Part Code: {part_code}")
        vlayout.addWidget(self.selected_part_label)
        
        self.e1 = QLineEdit()
        self.e1.setValidator(QIntValidator())
        self.e1.setMaxLength(5)
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

        self.reject_details = [
        "missing_components", "dented", "scratches", "sliver_streak", "ink_mark","incompleted", "dirty", "dust","fibre",
        "extra_screw", "extra_nanowl", "light_bubble"
        ]

        self.spin_boxes = {}

         # Populate grid with labels and spin boxes
        for i, detail in enumerate(self.reject_details):
            label = QLabel(detail.replace('_', ' ').capitalize())
            spin_box = QSpinBox()
            spin_box.setRange(0, 5000)  # Set range as needed
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
            self.submit_final_phase_checking()




    def submit_final_phase_checking(self):

         date_assemble = self.calender.selectedDate().toString("yyyy-MM-dd")
         assemble_output_amount = self.e1.text()
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
            
            sql_assemble_history = """
                    INSERT INTO history_assembly
                    (date_assemble, part_name, part_code, amount_inspect, amount_reject, parent_id, assembly_info_id, movement_reason, checker_name, date_entered) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                """
            assemble_history_inputs = (
            date_assemble,
            part_name,
            self.part_code,
            assemble_output_amount,
            total_defects if total_defects is not None else 0,
            parent_id,
            "200",
            self.assemble_id,
            checker
            )
            my_cursor.execute(sql_assemble_history, assemble_history_inputs)

            # Retrieve the new print_inspection_id
            my_cursor.execute("SELECT LAST_INSERT_ID();")
            last_assemble_inspection_id = my_cursor.fetchone()[0]

            # Insert defects into `print_defect_list` using the correct `print_inspection_id`
            sql_defect_list = """
            INSERT INTO assembly_defect_list
            (assembly_inspection_id,missing_components, dented, scratches, sliver_streak, ink_mark,incompleted, dirty, dust,fibre,
            extra_screw, extra_nanowl, light_bubble)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """

            values = (last_assemble_inspection_id,) + tuple(defect_data.get(defect, 0) for defect in self.reject_details) 
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

         self.b3 = QPushButton("Assembly")
         self.b3.setChecked(True)
         self.b3.clicked.connect(self.open_to_store_assembly)
         hlayout.addWidget(self.b3)  



        #  self.b3 = QPushButton("On Hold")
        #  self.b3.setChecked(True)
        #  self.b3.clicked.connect(self.open_to_store_onhold)
        #  hlayout.addWidget(self.b3)  

         self.setLayout(hlayout)
         self.open_to_store_spray_window = None
         self.open_to_store_print_window = None
         self.open_to_store_assembly_window = None
        #  self.open_to_store_onhold_window = None

    # def open_to_store_onhold (self):

    #     if self.open_to_store_onhold_window is None:
    #         self.open_to_store_onhold_window = to_store_onhold()

    #     self.open_to_store_onhold_window.show()
      
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

    def open_to_store_assembly (self):
          
        if self.open_to_store_assembly_window is None:
            self.open_to_store_assembly_window = to_store_assemble()
        
        # Show the open_new_batch_print_window window
        self.open_to_store_assembly_window.show()

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
        self.r3 = QRadioButton("On Hold")
        self.r3.setChecked(False)

        
        # Add radio buttons to horizontal layout
        hlayout.addWidget(self.r1)
        hlayout.addWidget(self.r2)
        hlayout.addWidget(self.r3)       
        # Add the horizontal layout with radio buttons to the main layout
        vlayout.addLayout(hlayout)

        # Connect radio buttons to the toggle handler
        self.r1.toggled.connect(self.on_radio_button_toggled)
        self.r2.toggled.connect(self.on_radio_button_toggled)
        self.r3.toggled.connect(self.on_radio_button_toggled)
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
        
        elif self.r2.isChecked() == True:
            query = """
                SELECT spray_batch_id, part_code, part_name, finished_goods_balance 
                FROM spray_batch_info 
                WHERE date_sprayed = %s
            """
        
        else:
            query = """
                SELECT spray_batch_id, part_code, part_name, on_hold 
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
        elif self.r2.isChecked():
            for spray_batch_id, part_code, part_name, finished_goods_balance in part_list:
                part_info = f"Spray Batch ID: {spray_batch_id}, Part Name: {part_name}, Part Code: {part_code}, 200% Balance: {finished_goods_balance}"
                self.listWidget.addItem(part_info)
        else:
            for spray_batch_id, part_code, part_name, on_hold in part_list:
                part_info = f"Spray Batch ID: {spray_batch_id}, Part Name: {part_name}, Part Code: {part_code}, On Hold Balance: {on_hold}"
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
        self.r3.setChecked(False)  # Set the first radio button as checked

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
        self.e1.setMaxLength(5)
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
            if self.to_store_spray_instance.r1.isChecked():
                movement_reason = "pn100"
            elif self.to_store_spray_instance.r2.isChecked():
                movement_reason = "pn200"
            else:
                movement_reason = "pn_onhold"

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
        self.r3 = QRadioButton("On Hold")
        self.r3.setChecked(False)

        
        # Add radio buttons to horizontal layout
        hlayout.addWidget(self.r1)
        hlayout.addWidget(self.r2)
        hlayout.addWidget(self.r3)
        
        # Add the horizontal layout with radio buttons to the main layout
        vlayout.addLayout(hlayout)

        # Connect radio buttons to the toggle handler
        self.r1.toggled.connect(self.on_radio_button_toggled)
        self.r2.toggled.connect(self.on_radio_button_toggled)
        self.r3.toggled.connect(self.on_radio_button_toggled)
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
        self.r3.setChecked(False)  # Set the first radio button as checked
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
        elif self.r2.isChecked() == True:
            query = """
                SELECT print_info_id, part_code, part_name, finished_good_balance 
                FROM print_batch_info 
                WHERE date_printed = %s
            """

        else:
            query = """
                SELECT print_info_id, part_code, part_name, on_hold 
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
        elif self.r2.isChecked():
            for print_info_id, part_code, part_name, finished_goods_balance in part_list:
                part_info = f"Print Batch ID: {print_info_id}, Part Name: {part_name}, Part Code: {part_code}, 200% Balance: {finished_goods_balance}"
                self.listWidget.addItem(part_info)
        else:
            for print_info_id, part_code, part_name, on_hold in part_list:
                part_info = f"Print Batch ID: {print_info_id}, Part Name: {part_name}, Part Code: {part_code}, On Hold Balance: {on_hold}"
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
        self.e1.setMaxLength(5)
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
            if self.to_store_print_instance.r1.isChecked():
                movement_reason = "pn100"
            elif self.to_store_print_instance.r2.isChecked():
                movement_reason = "pn200"
            else:
                movement_reason = "pn_onhold"

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
            # Commit to finalize the `print_defect_list` insert
            mydb.commit()
            print("Data Inserted")
            self.e1.clear()
            self.calender.setSelectedDate(QDate.currentDate())  # Reset the calendar to today's date

         except mysql.connector.Error as e:
            mydb.rollback()  # Roll back transaction in case of an error
            print(f"Error: {e}")



class to_store_assemble(QWidget):
    # Define the signal at the class level
    part_selected = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super(to_store_assemble, self).__init__(parent)
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
        self.r3 = QRadioButton("On Hold")
        self.r3.setChecked(False)

        
        # Add radio buttons to horizontal layout
        hlayout.addWidget(self.r1)
        hlayout.addWidget(self.r2)
        hlayout.addWidget(self.r3)       
        # Add the horizontal layout with radio buttons to the main layout
        vlayout.addLayout(hlayout)

        # Connect radio buttons to the toggle handler
        self.r1.toggled.connect(self.on_radio_button_toggled)
        self.r2.toggled.connect(self.on_radio_button_toggled)
        self.r3.toggled.connect(self.on_radio_button_toggled)
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
                SELECT assembly_info_id, part_code, part_name, hundered_balance 
                FROM assembly_batch_info 
                WHERE date_assemble = %s
            """
        
        elif self.r2.isChecked() == True:
            query = """
                SELECT assembly_info_id, part_code, part_name, finished_goods_balance 
                FROM assembly_batch_info 
                WHERE date_assemble = %s
            """
        
        else:
            query = """
                SELECT assembly_info_id, part_code, part_name, on_hold 
                FROM assembly_batch_info 
                WHERE date_assemble = %s
            """
        
        # Example for executing the query (assuming my_cursor and database connection exist)
        # Replace this with your actual database handling code
        my_cursor.execute(query, (date_str,))
        part_list = my_cursor.fetchall()

        
        # Populate list widget with parts information
        if self.r1.isChecked():
            for assembly_info_id, part_code, part_name, hundered_balance in part_list:
                part_info = f"Assemble Batch ID: {assembly_info_id}, Part Name: {part_name}, Part Code: {part_code}, 100% Balance: {hundered_balance}"
                self.listWidget.addItem(part_info)
        elif self.r2.isChecked():
            for assembly_info_id, part_code, part_name, finished_goods_balance in part_list:
                part_info = f"Assemble Batch ID: {assembly_info_id}, Part Name: {part_name}, Part Code: {part_code}, 200% Balance: {finished_goods_balance}"
                self.listWidget.addItem(part_info)
        else:
            for assembly_info_id, part_code, part_name, on_hold in part_list:
                part_info = f"Assemble Batch ID: {assembly_info_id}, Part Name: {part_name}, Part Code: {part_code}, On Hold Balance: {on_hold}"
                self.listWidget.addItem(part_info)

    def on_item_clicked(self, item):
        # Parse the spray ID and part code from the selected item text
        item_text = item.text()
        assemble_id = int(item_text.split(",")[0].split(":")[1].strip())
        part_code = item_text.split(",")[2].split(":")[1].strip()

        # Emit the signal and open the entry form with parsed spray_id and part_code
        self.part_selected.emit(assemble_id, part_code)  # Emit the signal

        # Optionally, call open_entry_form
        self.open_entry_form(assemble_id, part_code)

    def open_entry_form(self, assemble_id, part_code):
        # Check if the window is already open; if not, create it
        if self.open_entry_form_instance is None:
            self.open_entry_form_instance = open_to_store_assemble_entry(assemble_id, part_code, self)
        
        # Update the part label if the form is already open
        else:
            self.open_entry_form_instance.spray_id = assemble_id
            self.open_entry_form_instance.part_code = part_code
            self.open_entry_form_instance.selected_part_label.setText(f"Selected Part Code: {part_code}")

        # Show the window
        self.open_entry_form_instance.show()


    def reset_radio_buttons(self):
        self.r1.setChecked(True)  # Set the first radio button as checked
        self.r2.setChecked(False)  # Set the first radio button as checked
        self.r3.setChecked(False)  # Set the first radio button as checked

class open_to_store_assemble_entry(QWidget):
    def __init__(self, assemble_id, part_code,to_store_spray_instance, parent=None):
        super(open_to_store_assemble_entry, self).__init__(parent)

        self.assemble_id = assemble_id
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
        self.e1.setMaxLength(5)
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
            f"<b>Date Send To Store:</b> {date_checked}<br>"
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
            
            # Insert into `history_print` table
            sql_assemble_history = """
                    INSERT INTO history_assembly
                    (date_assemble, part_name, part_code, amount_inspect, amount_reject, parent_id, assembly_info_id, movement_reason, date_entered) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                """
            if self.to_store_spray_instance.r1.isChecked():
                movement_reason = "pn100"
            elif self.to_store_spray_instance.r2.isChecked():
                movement_reason = "pn200"
            else:
                movement_reason = "pn_onhold"

            assemble_history_inputs = (
                date_checked,
                part_name,
                self.part_code,
                checked_output_amount,
                total_defects if total_defects is not None else 0, 
                parent_id,
                self.assemble_id,
                movement_reason
            )

            """
            so here is insert into spray history first
            """
            my_cursor.execute(sql_assemble_history, assemble_history_inputs)

            mydb.commit()
            print("Data Inserted")

            self.e1.clear()
            self.calender.setSelectedDate(QDate.currentDate()) 

         except mysql.connector.Error as e:
            mydb.rollback()  
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
         self.e1.setMaxLength(5)
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
         self.reject_details = [
                "dust_marks","fibre_marks","paint_marks","white_marks","sink_marks","texture_marks","water_marks",
                "flow_marks","black_dot","white_dot","over_paint","under_spray","colour_out","masking_ng","flying_paint","weldline",
                "banding","short_mould","sliver_streak","dented","scratches","dirty"
         ]
         self.spin_boxes = {}

         # Populate grid with labels and spin boxes
         for i, detail in enumerate(self.reject_details):
               label = QLabel(detail.replace('_', ' ').capitalize())
               spin_box = QSpinBox()
               spin_box.setRange(0, 5000)  # Set range as needed
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

class delete_record(QWidget):
    def __init__(self,  parent=None):
        super(delete_record, self).__init__(parent)

        hlayout = QHBoxLayout()
    
        self.b1 = QPushButton("Spray")
        self.b1.setChecked(True)
        self.b1.clicked.connect(self.open_delete_record_spray)
        hlayout.addWidget(self.b1)
        
        self.b2 = QPushButton("Print")
        self.b2.setChecked(True)
        self.b2.clicked.connect(self.open_delete_record_print)
        hlayout.addWidget(self.b2)

        self.setLayout(hlayout)
        self.open_delete_record_spray_window = None
        self.open_delete_record_print_window = None


      
    def open_delete_record_spray (self):
          
        if self.open_delete_record_spray_window is None:
            self.open_delete_record_spray_window = delete_record()
        
        # Show the open_new_batch_print_window window
        self.open_delete_record_spray_window.show()


class delete_record(QWidget):
    # Define the signal at the class level
    part_selected = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super(delete_record, self).__init__(parent)
        self.open_entry_form_instance = None

        # Main vertical layout
        vlayout = QVBoxLayout()
        
        # Horizontal layout for radio buttons
        hlayout = QHBoxLayout()

        # Create radio buttons
        self.r1 = QRadioButton("Spray")
        self.r1.setChecked(True)
        self.r2 = QRadioButton("Print")
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
            # query = """
            #     SELECT spray_batch_id, part_code, part_name, hundered_balance 
            #     FROM spray_batch_info 
            #     WHERE date_sprayed = %s
            # """
            query = """
            SELECT spray_inspection_id, part_name, part_code, amount_inspect, amount_reject, movement_reason FROM history_spray
            WHERE DATE(date_entered) = %s
            """
        else:
            query = """
            SELECT print_inspection_id, part_name, part_code, amount_inspect, amount_reject, movement_reason FROM history_print
            WHERE DATE(date_entered) = %s
            """
        
        # Example for executing the query (assuming my_cursor and database connection exist)
        # Replace this with your actual database handling code
        my_cursor.execute(query, (date_str,))
        part_list = my_cursor.fetchall()
        # print(part_list)

        
        # Populate list widget with parts information
        if self.r1.isChecked():
            for spray_inspection_id, part_name, part_code, amount_inspect, amount_reject, movement_reason in part_list:
                part_info = f"Spray Inspection ID: {spray_inspection_id}, Part Name: {part_name}, Part Code: {part_code}, Amount Inspect: {amount_inspect}, Amount Reject: {amount_reject}, Movement Reason: {movement_reason}"
                self.listWidget.addItem(part_info)
        else:
            for print_inspection_id, part_name, part_code, amount_inspect, amount_reject, movement_reason in part_list:
                part_info = f"Print Inspection ID: {print_inspection_id}, Part Name: {part_name}, Part Code: {part_code}, Amount Inspect: {amount_inspect}, Amount Reject: {amount_reject}, Movement Reason: {movement_reason}"
                self.listWidget.addItem(part_info)

    def on_item_clicked(self, item):
        # Parse the spray ID and part code from the selected item text
        item_text = item.text()
        id = int(item_text.split(",")[0].split(":")[1].strip())

        # Emit the signal and open the entry form with parsed spray_id and part_code
        # self.part_selected.emit(id)  # Emit the signal
        print(id)
        # Optionally, call open_entry_form
        self.confirmation(item)
    
    def confirmation(self, item):
        item_text = item.text()
    
        # Set up the confirmation message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Confirm Delete Record?")
        msg.setInformativeText(
            item_text
        )
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # Capture the button clicked and proceed with submission only if OK is clicked
        if msg.exec_() == QMessageBox.Ok:
            self.delete_entry(item)
        

    def delete_entry(self, item):
        item_text = item.text()
        id = item_text.split(",")[0].split(":")[1].strip()
        if self.r1.isChecked():  
            query_defect_list = """
            DELETE FROM spray_defect_list WHERE spray_inspection_id = %s;
            """
            my_cursor.execute(query_defect_list, (id,))
        
            query_history = """
            DELETE FROM history_spray WHERE spray_inspection_id = %s;
            """
            my_cursor.execute(query_history, (id,))

            mydb.commit()
            print("Data Inserted")

        else:
            query_defect_list = """
            DELETE FROM print_defect_list WHERE print_inspection_id = %s;
            """
            my_cursor.execute(query_defect_list, (id,))
   
            query_history = """
            DELETE FROM history_print WHERE print_inspection_id = %s;
            """
            my_cursor.execute(query_history, (id,))

            mydb.commit()
            print("Data Deleted")

class QCOnHold(QWidget):

    """
        take from spray, print, assem
        take from 200% 


        so first page is spray, print, assem
        when click into any one of them 
        show date, date will query part code for that day

        click on part code
        enter details
    """

    def __init__(self, parent = None):
        super(QCOnHold,self).__init__(parent)

        hlayout = QHBoxLayout()


        self.b1 = QPushButton("Spray")
        self.b1.setChecked(True)
        self.b1.clicked.connect(self.open_qc_spray_window)
        hlayout.addWidget(self.b1)
        
        self.b2 = QPushButton("Print")
        self.b2.setChecked(True)
        self.b2.clicked.connect(self.open_qc_print_window)
        hlayout.addWidget(self.b2)

        self.b3 = QPushButton("Assembly")
        self.b3.setChecked(True)
        self.b3.clicked.connect(self.open_qc_assembly_window)
        hlayout.addWidget(self.b3)

        self.setLayout(hlayout)

        self.open_qc_spray = None
        self.open_qc_print = None
        self.open_qc_assembly = None

    def open_qc_spray_window(self):

        if self.open_qc_spray is None:
            self.open_qc_spray = qc_spray_window()
        
        # Show the open_new_batch_print_window window
        self.open_qc_spray.show()

    def open_qc_print_window(self):

        if self.open_qc_print is None:
            self.open_qc_print = qc_print_window()
        
        # Show the open_new_batch_print_window window
        self.open_qc_print.show()

    def open_qc_assembly_window(self):

        if self.open_qc_assembly is None:
            self.open_qc_assembly = qc_assembly_window()
        
        # Show the open_new_batch_print_window window
        self.open_qc_assembly.show()




class qc_spray_window(QWidget):
    part_selected = pyqtSignal(int, str)

    def __init__(self, parent = None):
        super(qc_spray_window,self).__init__(parent)
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
        self.open_entry_form_instance = None  # Renamed to avoid conflict with method
        
    def load_parts_for_date(self, selected_date):
        # Clear the list widget to refresh with new data
        self.listWidget.clear()

        # Convert QDate to string in format 'YYYY-MM-DD'
        date_str = selected_date.toString("yyyy-MM-dd")

        # Fetch data for the selected date
        query = """
        SELECT 
            spray_batch_info.spray_batch_id, 
            spray_batch_info.part_code, 
            spray_batch_info.part_name, 
            spray_batch_info.finished_goods_balance
        FROM 
            spray_batch_info
        INNER JOIN 
            history_spray 
            ON history_spray.spray_batch_id = spray_batch_info.spray_batch_id

        WHERE history_spray.movement_date = %s
        """
        my_cursor.execute(query, (date_str,))
        part_list = my_cursor.fetchall()
        print(part_list)

        # Populate list widget with parts information
        seen = set()

        for spray_batch_id, part_code, part_name, finished_goods_balance in part_list:
            part_info = f"Spray Batch ID: {spray_batch_id}, Part Name: {part_name}, Part Code: {part_code}, Balance: {finished_goods_balance}"
            
            if part_info not in seen:
                self.listWidget.addItem(part_info)
                seen.add(part_info)


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
            self.open_entry_form_instance = qc_spray_input_window(spray_id, part_code)
        
        # Update the part label if the form is already open
        else:
            self.open_entry_form_instance.spray_id = spray_id
            self.open_entry_form_instance.part_code = part_code
            self.open_entry_form_instance.selected_part_label.setText(f"Selected Part Code: {part_code}")

        # Show the window
        self.open_entry_form_instance.show()


class qc_spray_input_window(QWidget):
    def __init__(self, spray_id, part_code, parent=None):
        super(qc_spray_input_window,self).__init__(parent)

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
        self.e1.setMaxLength(5)
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
        self.reject_details = [
            "dust_marks","fibre_marks","paint_marks","white_marks","sink_marks","texture_marks","water_marks",
            "flow_marks","black_dot","white_dot","over_paint","under_spray","colour_out","masking_ng","flying_paint","weldline",
            "banding","short_mould","sliver_streak","dented","scratches","dirty"
        ]
        self.spin_boxes = {}

        # Populate grid with labels and spin boxes
        for i, detail in enumerate(self.reject_details):
            label = QLabel(detail.replace('_', ' ').capitalize())
            spin_box = QSpinBox()
            spin_box.setRange(0, 5000)  # Set range as needed
            self.spin_boxes[detail] = spin_box  # Store reference to each spin box

            grid.addWidget(label, i // 2, (i % 2) * 2)
            grid.addWidget(spin_box, i // 2, (i % 2) * 2 + 1)

    
        hlayout.addLayout(vlayout)
        hlayout.addLayout(grid)
        self.setLayout(hlayout)
    
    def test(self):
        print("hi")

    def clear_defect_details(self):
            # Clear all spin boxes in the reject details
            for spin_box in self.spin_boxes.values():
                spin_box.setValue(0)  # Reset each spin box value to 0



    def confirmation(self):
        print("HI")
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
            self.submit_qc_spray()

    def submit_qc_spray(self):

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
                    "onhold",
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






# class qc_print_input_window(QWidget):
#     def __init__(self, part_codes, parent = None):
#         super(qc_print_input_window,self).__init__(parent)

# class qc_assembly_input_window(QWidget):
#     def __init__(self, part_codes, parent = None):
#         super(qc_assembly_input_window,self).__init__(parent)
        
##########################################################################################


class qc_print_window(QWidget):
    part_selected = pyqtSignal(int, str)

    def __init__(self, parent = None):
        super(qc_print_window,self).__init__(parent)
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
        self.open_entry_form_instance = None  # Renamed to avoid conflict with method
        
    def load_parts_for_date(self, selected_date):
        # Clear the list widget to refresh with new data
        self.listWidget.clear()

        # Convert QDate to string in format 'YYYY-MM-DD'
        date_str = selected_date.toString("yyyy-MM-dd")

        # Fetch data for the selected date
        query = """
        SELECT 
            print_batch_info.print_info_id, 
            print_batch_info.part_code, 
            print_batch_info.part_name, 
            print_batch_info.finished_good_balance
        FROM 
            print_batch_info
        INNER JOIN 
            history_print
            ON history_print.print_info_id = print_batch_info.print_info_id

        WHERE history_print.date_print = %s
        """
        my_cursor.execute(query, (date_str,))
        part_list = my_cursor.fetchall()
        print(part_list)

        # Populate list widget with parts information
        seen = set()

        for print_info_id, part_code, part_name, finished_goods_balance in part_list:
            part_info = f"Print Batch ID: {print_info_id}, Part Name: {part_name}, Part Code: {part_code}, Balance: {finished_goods_balance}"
            
            if part_info not in seen:
                self.listWidget.addItem(part_info)
                seen.add(part_info)


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
            self.open_entry_form_instance = qc_print_input_window(print_id, part_code)
        
        # Update the part label if the form is already open
        else:
            self.open_entry_form_instance.print_id = print_id
            self.open_entry_form_instance.part_code = part_code
            self.open_entry_form_instance.selected_part_label.setText(f"Selected Part Code: {part_code}")

        # Show the window
        self.open_entry_form_instance.show()


class qc_print_input_window(QWidget):
    def __init__(self, print_id, part_code, parent=None):
        super(qc_print_input_window,self).__init__(parent)

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
        self.e1.setMaxLength(5)
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
        self.reject_details = [
        "dust_marks", "dust_fibre", "black_dot", "dust_paint", "thiner_mark", "incompleted", 
        "banding", "ink_mark", "under_spray", "shining", "position_out", "smear", "adjustment", 
        "scratches", "dirty", "dprinting", "white_dot", "dented", "bubble", "sink_mark", 
        "bulging", "short_mould", "weldline", "colour_out", "gate_high", "over_stamp", "overtrim"
    ]
        self.spin_boxes = {}

        # Populate grid with labels and spin boxes
        for i, detail in enumerate(self.reject_details):
            label = QLabel(detail.replace('_', ' ').capitalize())
            spin_box = QSpinBox()
            spin_box.setRange(0, 5000)  # Set range as needed
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
            self.submit_qc_print()

    def submit_qc_print(self):

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
                "onhold",
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
                (print_inspection_id, dust_mark, dust_fibre, black_dot, dust_paint, thiner_mark, incompleted, banding, ink_mark, under_spray,
                shining, position_out, smear,   adjustment,   scratches, dirty, dprinting,  white_dot, dented, bubble,  
                sink_mark, bulging, short_mould, weldline,  colour_out, gate_high, over_stamp, overtrim)
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

#####################################################################################################################################################


class qc_assembly_window(QWidget):
    part_selected = pyqtSignal(int, str)

    def __init__(self, parent = None):
        super(qc_assembly_window,self).__init__(parent)
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
        self.open_entry_form_instance = None  # Renamed to avoid conflict with method
        
    def load_parts_for_date(self, selected_date):
        # Clear the list widget to refresh with new data
        self.listWidget.clear()

        # Convert QDate to string in format 'YYYY-MM-DD'
        date_str = selected_date.toString("yyyy-MM-dd")

        # Fetch data for the selected date
        query = """
        SELECT 
            assembly_batch_info.assembly_info_id, 
            assembly_batch_info.part_code, 
            assembly_batch_info.part_name, 
            assembly_batch_info.finished_goods_balance
        FROM 
            assembly_batch_info
        INNER JOIN 
            history_assembly
            ON history_assembly.assembly_info_id = assembly_batch_info.assembly_info_id

        WHERE history_assembly.date_assemble = %s
        """
        my_cursor.execute(query, (date_str,))
        part_list = my_cursor.fetchall()
        print(part_list)

        # Populate list widget with parts information
        seen = set()

        for print_info_id, part_code, part_name, finished_goods_balance in part_list:
            part_info = f"Assemble Batch ID: {print_info_id}, Part Name: {part_name}, Part Code: {part_code}, Balance: {finished_goods_balance}"
            
            if part_info not in seen:
                self.listWidget.addItem(part_info)
                seen.add(part_info)


    def on_item_clicked(self, item):
        # Parse the spray ID and part code from the selected item text
        item_text = item.text()
        assemble_id = item_text.split(",")[0].split(":")[1].strip()
        part_code = item_text.split(",")[2].split(":")[1].strip()

        # Emit the signal and open the entry form with parsed spray_id and part_code
        self.part_selected.emit(int(assemble_id), part_code)  # Emit the signal

        # Optionally, call open_entry_form
        self.open_entry_form(assemble_id, part_code)

    def open_entry_form(self, assemble_id, part_code):
        # Check if the window is already open; if not, create it
        if self.open_entry_form_instance is None:
            self.open_entry_form_instance = qc_print_input_window(assemble_id, part_code)
        
        # Update the part label if the form is already open
        else:
            self.open_entry_form_instance.assemble_id = assemble_id
            self.open_entry_form_instance.part_code = part_code
            self.open_entry_form_instance.selected_part_label.setText(f"Selected Part Code: {part_code}")

        # Show the window
        self.open_entry_form_instance.show()


class qc_print_input_window(QWidget):
    def __init__(self, assemble_id, part_code, parent=None):
        super(qc_print_input_window,self).__init__(parent)

        self.assemble_id = assemble_id
        self.part_code = part_code

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        grid = QGridLayout()

        # Output amount
        self.selected_part_label = QLabel(f"Selected Part Code: {part_code}")
        vlayout.addWidget(self.selected_part_label)
        
        self.e1 = QLineEdit()
        self.e1.setValidator(QIntValidator())
        self.e1.setMaxLength(5)
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
        self.reject_details = [
        "missing_components", "dented", "scratches", "sliver_streak", "ink_mark","incompleted", "dirty", "dust","fibre",
        "extra_screw", "extra_nanowl", "light_bubble"
        ]
        self.spin_boxes = {}

        # Populate grid with labels and spin boxes
        for i, detail in enumerate(self.reject_details):
            label = QLabel(detail.replace('_', ' ').capitalize())
            spin_box = QSpinBox()
            spin_box.setRange(0, 5000)  # Set range as needed
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
            self.submit_qc_print()

    def submit_qc_print(self):

            date_assemble = self.calender.selectedDate().toString("yyyy-MM-dd")
            assemble_output_amount = self.e1.text()
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


                sql_assemble_history = """
                    INSERT INTO history_assembly
                    (date_assemble, part_name, part_code, amount_inspect, amount_reject, parent_id, assembly_info_id, movement_reason, checker_name, date_entered) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                """
                assemble_history_inputs = (
                    date_assemble,
                    part_name,
                    self.part_code,
                    assemble_output_amount,
                    total_defects if total_defects is not None else 0,
                    parent_id,
                    self.assemble_id,  # Using the fetched `print_info_id`
                    "on hold",
                    checker
                )
                my_cursor.execute(sql_assemble_history, assemble_history_inputs)

                # Retrieve the new print_inspection_id
                my_cursor.execute("SELECT LAST_INSERT_ID();")
                last_print_inspection_id = my_cursor.fetchone()[0]

                # Insert defects into `print_defect_list` using the correct `print_inspection_id`
                sql_defect_list = """
                INSERT INTO assembly_defect_list
                (assembly_inspection_id,missing_components, dented, scratches, sliver_streak, ink_mark,incompleted, dirty, dust,fibre,
                extra_screw, extra_nanowl, light_bubble)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
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






class assembly_window (QWidget):
    def __init__(self,part_codes, parent = None):
        super(assembly_window ,self).__init__(parent)
        self.part_codes = part_codes

        self.setWindowTitle("Enter New Print Batch")
        layout = QHBoxLayout()
        
        self.b1 = QPushButton("From Injection Batch")
        self.b1.setCheckable(True)
        self.b1.clicked.connect(self.new_injection_batch_entry_window)
        layout.addWidget(self.b1)

        self.b2 = QPushButton("Take From Print")
        self.b2.setCheckable(True)
        self.b2.clicked.connect(self.take_from_print_entry_window)
        layout.addWidget(self.b2)

        self.setLayout(layout)

        self.new_injection_batch_entry_window = None
        self.take_from_print_entry_window = None
    
    def new_injection_batch_entry_window(self):
        if self.new_injection_batch_entry_window is None:
            self.new_injection_batch_entry_window = new_injection_batch_entry_window(self.part_codes)
        
        # Show the new_print_batch_entry_window window
        self.new_injection_batch_entry_window.show()

    def take_from_print_entry_window(self):
        if self.take_from_print_entry_window is None:
            self.take_from_print_entry_window = take_from_print()
        
        # Show the new_print_batch_entry_window window
        self.take_from_print_entry_window.show()

class new_injection_batch_entry_window(QWidget):
    def __init__(self, part_codes, parent = None):
        super(new_injection_batch_entry_window,self).__init__(parent)

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
        self.e1.setMaxLength(5)
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
        "missing_components", "dented", "scratches", "sliver_streak", "ink_mark","incompleted", "dirty", "dust","fibre",
        "extra_screw", "extra_nanowl", "light_bubble"
        ]

        self.spin_boxes = {}

        # Populate grid with labels and line edits
        for i, detail in enumerate(self.reject_details):
            label = QLabel(detail.replace('_', ' ').capitalize())
            spin_box = QSpinBox()
            spin_box.setRange(0, 5000)  # Set range as needed
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
            f"<b>Total Assemble:</b> {print_output_amount}<br>"
            f"<b>Total Rejected:</b> {sum(non_zero_defects.values())}<br>"
            f"<b>Date Assemble:</b> {date_print}<br>"
            f"<b>Checker:</b> {checker}<br><br>"
            f"<b>Rejection Details:</b><br>{rejection_details_text if rejection_details_text else 'None'}"
        )
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # Capture the button clicked and proceed with submission only if OK is clicked
        if msg.exec_() == QMessageBox.Ok:
            self.submit_new_assembly_batch()

    def submit_new_assembly_batch(self):
        
      part_code = self.part_code_entry.currentText()
      assemble_output_amount = self.e1.text()
      date_assemble = self.calender.selectedDate().toString("yyyy-MM-dd")
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
         INSERT INTO assembly_batch_info 
         (part_name, part_code, parent_id, date_assemble, batch_status)
         VALUES (%s, %s, %s, %s, %s)
         """
         print_batch_input = (
            part_name,
            part_code,
            parent_id,
            date_assemble,
            "incomplete"
         )
         my_cursor.execute(sql_print_batch_info, print_batch_input)

         # Fetch the newly generated `print_info_id`
         my_cursor.execute("SELECT LAST_INSERT_ID();")
         last_assembly_info_id = my_cursor.fetchone()[0]

         if self.cb1.isChecked():
            # Insert into `history_print` table
            sql_history_assemble = """
                INSERT INTO history_assembly
                (date_assemble , part_name, part_code, amount_inspect, amount_reject, parent_id, assembly_info_id, movement_reason, checker_name, date_entered) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            assemble_history_inputs = (
                date_assemble,
                part_name,
                part_code,
                assemble_output_amount,
                total_defects if total_defects is not None else 0,
                parent_id,
                last_assembly_info_id,  # Using the fetched `print_info_id`
                "Secondary process",
                checker
            )
         else:
            sql_history_assemble = """
                INSERT INTO history_assembly
                (date_assemble , part_name, part_code, amount_inspect, amount_reject, parent_id, assembly_info_id, movement_reason, checker_name, date_entered) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            assemble_history_inputs = (
                date_assemble,
                part_name,
                part_code,
                assemble_output_amount,
                total_defects if total_defects is not None else 0,
                parent_id,
                last_assembly_info_id,  # Using the fetched `print_info_id`
                "New Assembly batch",
                checker
            )
         
         my_cursor.execute(sql_history_assemble, assemble_history_inputs)


         # Fetch the last inserted `print_inspection_id`
         my_cursor.execute("SELECT LAST_INSERT_ID();")
         last_print_inspection_id = my_cursor.fetchone()[0]

         # Insert into `print_defect_list` using `last_print_inspection_id`
         sql = """
            INSERT INTO assembly_defect_list
            (assembly_inspection_id,missing_components, dented, scratches, sliver_streak, ink_mark,incompleted, dirty, dust,fibre,
        extra_screw, extra_nanowl, light_bubble)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
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






class take_from_print(QWidget):
    # Define the signal that will be emitted
    part_selected = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super(take_from_print, self).__init__(parent)
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
            SELECT print_info_id, part_code, part_name, hundered_balance, total_output
            FROM print_batch_info 
            WHERE date_printed = %s
        """
        my_cursor.execute(query, (date_str,))
        part_list = my_cursor.fetchall()

        # Populate list widget with parts information
        for print_info_id, part_code, part_name, hundered_balance, total_output in part_list:
            # Use total_output as unchecked_balance if unchecked_balance is None
            display_balance = hundered_balance if hundered_balance is not None else total_output
            part_info = f"Print Batch ID: {print_info_id}, Part Name: {part_name}, Part Code: {part_code}, Hundered Balance: {display_balance}"
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
               self.open_entry_form_instance = open_take_from_print_entry(print_id, part_code)
         
         # Update the part label if the form is already open
         else:
               self.open_entry_form_instance.print_id = print_id
               self.open_entry_form_instance.part_code = part_code
               self.open_entry_form_instance.selected_part_label.setText(f"Selected Part Code: {part_code}")

         # Show the window
         self.open_entry_form_instance.show()


class open_take_from_print_entry(QWidget):
      def __init__(self, print_id, part_code, parent=None):
         super(open_take_from_print_entry, self).__init__(parent)

         my_cursor.execute("SELECT part_name, part_code FROM main_parts")
         all_parts_variant_info = my_cursor.fetchall()
         parts_tuple_variant = namedtuple("parts_info", ["part_name", "part_code"])
         # Create a list of named tuples for the parts
         parts_variant = [parts_tuple_variant(*part) for part in all_parts_variant_info]
         self.parts_variant = [part.part_code for part in parts_variant]  # Fix here

         self.print_id = print_id
         self.part_code = part_code

         vlayout = QVBoxLayout()
         hlayout = QHBoxLayout()
         grid = QGridLayout()

         # Output amount
         self.selected_part_label = QLabel(f"Selected Part Code: {part_code}")
         vlayout.addWidget(self.selected_part_label)

         self.part_code_entry = ExtendedComboBox()
         self.part_code_entry.addItems(self.parts_variant)  # Use corrected attribute
         vlayout.addWidget(self.part_code_entry)
         
         self.e1 = QLineEdit()
         self.e1.setValidator(QIntValidator())
         self.e1.setMaxLength(5)
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
         self.reject_details = [
        "missing_components", "dented", "scratches", "sliver_streak", "ink_mark","incompleted", "dirty", "dust","fibre",
        "extra_screw", "extra_nanowl", "light_bubble"
        ]

         self.spin_boxes = {}

         # Populate grid with labels and spin boxes
         for i, detail in enumerate(self.reject_details):
            label = QLabel(detail.replace('_', ' ').capitalize())
            spin_box = QSpinBox()
            spin_box.setRange(0, 5000)  # Set range as needed
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

      def confirmation(self):
            part_code = self.part_code
            print_output_amount = self.e1.text()
            date_print = self.calender.selectedDate().toString("yyyy-MM-dd")
            checker = self.e2.text().upper()
            variant_part = self.part_code_entry.currentText()

            # Collect non-zero rejection details
            non_zero_defects = {detail: spin_box.value() for detail, spin_box in self.spin_boxes.items() if spin_box.value() > 0}

            # Format non-zero rejection details for display using HTML for better alignment
            rejection_details_text = "<br>".join([f"{detail.replace('_', ' ').capitalize()}: {value}" for detail, value in non_zero_defects.items()])

            # Set up the confirmation message
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Please confirm entered values")
            msg.setInformativeText(
                f"<b>Part Code:</b> {variant_part}<br>"
                f"<b>Total Assembled:</b> {print_output_amount}<br>"
                f"<b>Total Rejected:</b> {sum(non_zero_defects.values())}<br>"
                f"<b>Date Assemble:</b> {date_print}<br>"
                f"<b>Checker:</b> {checker}<br><br>"
                f"<b>Rejection Details:</b><br>{rejection_details_text if rejection_details_text else 'None'}"
            )
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            # Capture the button clicked and proceed with submission only if OK is clicked
            if msg.exec_() == QMessageBox.Ok:
                self.submit_take_from_print()

    
      def submit_take_from_print(self):

        date_assemble = self.calender.selectedDate().toString("yyyy-MM-dd")
        assemble_output_amount = self.e1.text()
        defect_data = {}
        total_defects = 0
        checker = self.e2.text().upper()
        variant_part = self.part_code_entry.currentText()
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
                    "SELECT assembly_info_id, part_code FROM assembly_batch_info WHERE print_info_id = %s",
                    (self.print_id,)
                )
            result = my_cursor.fetchone()


            if result:
                last_print_info_id, existing_part_code = result  # Unpack values
                print("Batch exists, checking part_code...")

                my_cursor.fetchall()  # Clears any unread results

                if existing_part_code == variant_part:
                    print("✅ Part code matches, using existing print_info_id:", last_print_info_id)
                else:
                    print("⚠️ Part code mismatch, inserting a new row...")

                    # 🛠 Fix: Fetch any unread results to clear the cursor
                    my_cursor.fetchall()  # ✅ Ensures all rows are read before INSERT

                    sql_assemble_batch_info = """
                    INSERT INTO assembly_batch_info 
                    (part_name, part_code, parent_id, print_info_id, date_assemble, batch_status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """

                    assemble_batch_input = (
                        part_name,
                        variant_part,
                        parent_id,
                        self.print_id,
                        date_assemble,
                        "incomplete"
                    )

                    my_cursor.execute(sql_assemble_batch_info, assemble_batch_input)
                    last_assemble_info_id = my_cursor.lastrowid  # ✅ Get new print_info_id

                    print("✅ New print_info_id created:", last_assemble_info_id)

            else:
                print("🚀 No existing batch, inserting a new row...")

                sql_assemble_batch_info = """
                INSERT INTO assembly_batch_info 
                    (part_name, part_code, parent_id, print_info_id, date_assemble, batch_status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """

                assemble_batch_input = (
                        part_name,
                        variant_part,
                        parent_id,
                        self.print_id,
                        date_assemble,
                        "incomplete"
                    )

                my_cursor.execute(sql_assemble_batch_info, assemble_batch_input)
                last_assemble_info_id = my_cursor.lastrowid  # ✅ Get new print_info_id

                print("✅ New print_info_id created:", last_assemble_info_id)

            if self.cb1.isChecked():
                # Insert into `history_print` table
                sql_assemble_history = """
                    INSERT INTO history_assembly
                    (date_assemble, part_name, part_code, amount_inspect, amount_reject, parent_id, assembly_info_id, movement_reason, checker_name, date_entered) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                """
                assemble_history_inputs = (
                    date_assemble,
                    part_name,
                    variant_part,
                    assemble_output_amount,
                    total_defects if total_defects is not None else 0,
                    parent_id,
                    last_assemble_info_id,  # Using the fetched `print_info_id`
                    "Secondary process",
                    checker
                )
            else:
                sql_assemble_history = """
                    INSERT INTO history_assembly
                    (date_assemble, part_name, part_code, amount_inspect, amount_reject, parent_id, assembly_info_id, movement_reason, checker_name, date_entered) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                """
                assemble_history_inputs = (
                    date_assemble,
                    part_name,
                    variant_part,
                    assemble_output_amount,
                    total_defects if total_defects is not None else 0,
                    parent_id,
                    last_assemble_info_id,  # Using the fetched `print_info_id`
                    "New Assembly Batch",
                    checker
                )
            my_cursor.execute(sql_assemble_history, assemble_history_inputs)

            # Retrieve the new print_inspection_id
            my_cursor.execute("SELECT LAST_INSERT_ID();")
            last_print_inspection_id = my_cursor.fetchone()[0]

            # Insert into `history_spray` table
            sql_print_history = """
            INSERT INTO history_print
            (date_print, part_name, part_code, amount_inspect, amount_reject, parent_id, print_info_id, movement_reason, checker_name, date_entered) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            print_history_inputs = (
            date_assemble,
            part_name,
            variant_part,
            assemble_output_amount,
            total_defects,
            parent_id,
            self.print_id,
            "assemble",
            checker
            )
            my_cursor.execute(sql_print_history, print_history_inputs)
            my_cursor.execute("SELECT LAST_INSERT_ID();")
            last_print_inspection_id = my_cursor.fetchone()[0]

            # Insert defects into `print_defect_list` using the correct `print_inspection_id`
            sql_defect_list = """
            INSERT INTO assembly_defect_list
            (assembly_inspection_id,missing_components, dented, scratches, sliver_streak, ink_mark,incompleted, dirty, dust,fibre,
            extra_screw, extra_nanowl, light_bubble)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """

            values = (last_print_inspection_id,) + tuple(defect_data.get(defect, 0) for defect in self.reject_details) 
            my_cursor.execute(sql_defect_list, values)

            sql_spray_defect_list = """
                INSERT INTO print_defect_list
                (print_inspection_id, assembly_defect)
                VALUES(%s, %s)
                """
            values2 = (last_print_inspection_id, total_defects if total_defects is not None else 0 )
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





"""

take from print 
checkbox with secondary process

normal (take from injection)



"""


def main():
   app = QApplication([])
   ex = main_menu()
   ex.show()
   sys.exit(app.exec_())
if __name__ == '__main__':
   main()





