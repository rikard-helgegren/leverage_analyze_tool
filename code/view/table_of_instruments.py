
import tkinter as tk

#Make this a class
def __init__(self):
    frame = tk.Frame(self, padx=5, pady=5)
    frame.pack(side=tk.LEFT)
    #scrollbar
    game_scroll = tk.Scrollbar(frame)
    game_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    columns = ('country', 'leverage')

    self.market_table = tk.ttk.Treeview(frame,
                                        yscrollcommand=game_scroll.set,
                                        columns=columns,
                                        selectmode="extended")
    self.market_table.heading('#0', text='Text')
    self.market_table.heading('country', text='Country')
    self.market_table.heading('leverage', text='Leverage')
    self.market_table.pack()
    self.market_table.bind('<<TreeviewSelect>>',self.update_table_item_focused)


    # Define the row colors with a tag
    self.market_table.tag_configure("selected_row", background="green")
    self.market_table.tag_configure("not_selected_row", background="white")

    self.rows_unfolded = []


def set_market_table(self, names, countries):
    print("TRACE: table_of_instruments: set_market_table")

    all_item_values = get_all_item_values(self)
    all_item_texts = get_all_item_texts(self)

    added_new_item = False

    for market_name, country in zip(names, countries):
        #only add if market not in table
        if market_name not in all_item_texts:

            added_new_item = True

            self.market_table.insert(parent='', index=tk.END, iid=market_name, text=market_name, values=(country,1))
            for i in range(2,4): #leverage span
                self.market_table.insert(parent=market_name, index=tk.END, text=market_name, values=(country,i))

    if added_new_item:
        update_unfolding_status(self)


def get_table_item_focused(self):
    print("TRACE: table_of_instruments: get_table_item_focused")
    curItem = self.market_table.focus()
    item = self.market_table.item(curItem)

    return [item['text'], item['values'][1]] #market index and leverage


def update_item_color(self):
    print("TRACE: table_of_instruments: update_item_color")

    curItem = self.market_table.focus()
    current_item_tag = self.market_table.item(curItem)["tags"]

    if current_item_tag != ['selected_row']:
        self.market_table.item(curItem, tag="selected_row")
    else:
        self.market_table.item(curItem, tag="not_selected_row")


def get_all_item_texts(self):
    print("TRACE: table_of_instruments: get_all_item_texts")

    all_item_texts = []

    for item in self.market_table.get_children():
        item_text = self.market_table.item(item)['text']
        all_item_texts.append(item_text)

    return all_item_texts


def get_all_item_values(self):
    print("TRACE: table_of_instruments: get_all_item_values")

    all_item_values = []

    for item in self.market_table.get_children():
        item_value = self.market_table.item(item)['values']
        all_item_values.append(item_value[0]) # TODO update when adding bull > 1

    return all_item_values


def update_unfolding_status(self):
    print("TRACE: View: update_unfolding_status")

    rows_folding_status = []
    for item in self.market_table.get_children():
        item =  self.market_table.item(item)['open']

        rows_folding_status.append(item)
    self.rows_unfolded = rows_folding_status


def only_did_unfolding(self):
    rows_folding_status = []
    for item in self.market_table.get_children():
        item =  self.market_table.item(item)['open']

        rows_folding_status.append(item)


    if rows_folding_status == self.rows_unfolded:
        # Folding sattus unchanged, action was no unfolding
        self.rows_unfolded = rows_folding_status
        return False
    else:
        # Folding sattus changed, action was an unfolding
        self.rows_unfolded = rows_folding_status
        return True

