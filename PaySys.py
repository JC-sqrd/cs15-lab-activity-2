from abc import ABC, abstractmethod 
import tkinter as tk
from tkinter import messagebox

#@author Julio Caesar Tadena

class Payment(ABC):

    def __init__(self):
        self.__payer_name__ : str = ""
        self.final_amount : float = 0
        self.payment_data : dict = {}

    @abstractmethod
    def pay(self, amount : float) -> bool:
        return False
    
    def payment_info(self) -> dict:
        return self.payment_data

    def get_payer_name(self) -> str:
        return self.__payer_name__

    pass

class CashPayment(Payment):

    def pay(self, amount : float) -> bool:
        if amount > 0:
            return True
        return False
    
    pass

class CardPayment(Payment):
    
    def __init__(self):
        super().__init__()
        self.card_number : int = 0

    def pay(self, amount : float) -> bool:
        if amount > 0:
            return True
        return False
    
    pass


class MainModule():
    def __init__(self):
        self.payment_data : dict = {}
        self.label_font_size : int = 12

        self.root : tk.Tk = tk.Tk()
        self.root.title("Payment System")
        self.root.geometry("300x200")

        self.paysys_label : tk.Label = tk.Label(self.root, text="Payment System", font=('Arial', 16))
        self.paysys_label.pack()

        self.payer_label : tk.Label = tk.Label(self.root, text="Payer Name", font=('Arial', self.label_font_size))
        self.payer_label.pack()

        self.payer_name_var : tk.StringVar = tk.StringVar()
        self.payer_entry : tk.Entry = tk.Entry(self.root, textvariable=self.payer_name_var)
        self.payer_entry.pack()

        self.amount_label : tk.Label = tk.Label(self.root, text="Pay Amount", font=('Arial', self.label_font_size))
        self.amount_label.pack()

        self.amount_entry_var : tk.StringVar = tk.StringVar()
        self.amount_entry : tk.Entry = tk.Entry(self.root,textvariable=self.amount_entry_var)
        self.amount_entry.pack()

        self.radio_button_frame : tk.Frame = tk.Frame(self.root)
        self.radio_button_frame.pack()

        self.payment_state_var : tk.IntVar = tk.IntVar()
        self.cash_state_var : tk.IntVar = tk.IntVar()

        self.card_radio_button : tk.Radiobutton = tk.Radiobutton(self.radio_button_frame, text="Card", variable=self.payment_state_var, value=0)
        self.card_radio_button.grid(column=0, row=0)

        self.cash_radio_button : tk.Radiobutton = tk.Radiobutton(self.radio_button_frame, text="Cash", variable=self.payment_state_var, value=1)
        self.cash_radio_button.grid(column=1, row=0)

        self.pay_button : tk.Button = tk.Button(self.root, text="Pay", command=self.pay)
        self.pay_button.pack()
        
        self.root.mainloop()
        pass

    def pay(self):
        self.payment_data['payer_name'] = self.payer_name_var.get()

        try:
            self.payment_data['pay_amount'] = int(self.amount_entry_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount value")
            return
        
        payment_method = self.payment_state_var.get()
        if payment_method == 0:
            #Card Payment
            card_payment_module = CardPaymentModule(self.payment_data, self.root)
        elif payment_method == 1:
            #Cash Payment
            cash_payment_module = CashPaymentModule(self.payment_data, self.root)
        pass
    pass


class PaymentModule():
    def __init__(self, payment_data : dict, root : tk.Tk):
        self.payment_data : dict= payment_data
        self.pay_window : tk.Toplevel = tk.Toplevel(root)
        pass
    pass

class CashPaymentModule(PaymentModule):
    def __init__(self, payment_data, root):
        
        self.payment_data : dict= payment_data

        self.cash_payment : CashPayment = CashPayment()
        self.cash_payment.__payer_name__ = payment_data["payer_name"]
        self.cash_payment.final_amount = payment_data["pay_amount"]

        self.pay_with_cash()
    
    def pay_with_cash(self):
        self.cash_payment.payment_data = self.payment_data
        if self.cash_payment.pay(self.payment_data["pay_amount"]):
            name : str = self.cash_payment.__payer_name__
            paid_amount : int = self.cash_payment.final_amount
            formatted_string : str = f"\n\nPayment info: \nPayer Name: {name} \nPaid Amount: {paid_amount}"
            messagebox.showinfo("Success", "Payment processed!" + formatted_string)
            print("Payment processed!" + formatted_string)
        else:
            messagebox.showerror("Something went wrong", "Please make sure all values are valid")
        pass
    pass


class CardPaymentModule(PaymentModule):
    def __init__(self, payment_data, root):
        super().__init__(payment_data, root)

        self.label_font_size = 12

        self.card_payment : CardPayment = CardPayment()
        self.card_payment.__payer_name__ = payment_data["payer_name"]
        self.card_payment.final_amount = payment_data["pay_amount"]

        self.pay_window.title("Card Payment")
        self.pay_window.geometry("300x200")

        self.card_payment_label : tk.Label = tk.Label(self.pay_window, text="Card Payment", font=('Arial', 16))
        self.card_payment_label.pack()

        self.card_number_label : tk.Label = tk.Label(self.pay_window, text="Card Number", font=('Arial', self.label_font_size))
        self.card_number_label.pack()

        self.card_number_var : tk.StringVar = tk.StringVar()
        self.card_number_entry : tk.Entry = tk.Entry(self.pay_window, textvariable=self.card_number_var)
        self.card_number_entry.pack()

        self.pay_with_card_button : tk.Button = tk.Button(self.pay_window, text="Pay with Card", command=self.pay_with_card)
        self.pay_with_card_button.pack()

    def pay_with_card(self):
        try:
            self.payment_data["card_number"] = int(self.card_number_var.get()) 
            self.card_payment.card_number = self.payment_data["card_number"]
        except ValueError:
            messagebox.showerror("Error", "Invalid card number value")
            self.pay_window.focus()
            return
        self.card_payment.payment_data = self.payment_data
        if self.card_payment.pay(self.payment_data["pay_amount"]):
            name : str = self.card_payment.__payer_name__
            paid_amount : int = self.card_payment.final_amount
            card_number : int = self.card_payment.card_number
            formatted_string : str = f"\n\nPayment info: \nPayer Name: {name} \nPaid Amount: {paid_amount} \nCard Number: {card_number}"
            messagebox.showinfo("Success", "Payment processed!" + formatted_string)
            print("Payment processed!" + formatted_string)
            self.pay_window.destroy()
        else:
            messagebox.showerror("Something went wrong", "Please make sure all values are valid")
        pass
    pass

def main():
    main_module = MainModule()
    pass

main()