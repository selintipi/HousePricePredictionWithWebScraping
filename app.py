import flet as ft
import pickle
import numpy as np
import warnings
warnings.filterwarnings("ignore")

counter = 0

def main(page):
    ilcejson = {"Adalar":0,"Arnavutköy":1,"Ataşehir":2}

    regressor = pickle.load(open("model.sav", 'rb'))
    
    dd = ft.Dropdown(
        width=250,
        options=[
            ft.dropdown.Option("Adalar"),
            ft.dropdown.Option("Arnavutköy"),
            ft.dropdown.Option("Ataşehir"),
        ],
    )
    dd.value = "Adalar"
    ddtext = ft.Text(value="İLÇELER ")
    oda = ft.TextField(label="Oda Sayısı")
    salon = ft.TextField(label="Salon Sayısı")
    brut = ft.TextField(label="Brut m2")
    net = ft.TextField(label="Net m2")
    yas = ft.TextField(label="Bina Yaşı")
    banyo = ft.TextField(label="Banyo Sayısı")
    greetings = ft.Column()

    def btn_click(e):
        global counter
        id = ilcejson[dd.value]
        ev = np.array([[id, oda.value, salon.value, brut.value, net.value, yas.value, banyo.value]], dtype=np.int64)
        ev_pred = regressor.predict(ev)
        pred_val = ft.Text(f"Tahmini fiyat = {int(ev_pred[0])}")
        if(counter==0):
            pred_val = ft.Text(f"Tahmini fiyat = {int(ev_pred[0])}")
            greetings.controls.append(pred_val)
            counter = counter + 1
        else:
            greetings.controls.pop()
            greetings.controls.append(pred_val)
            
        page.update()

        oda.value = ""
        salon.value = ""
        brut.value = ""
        net.value = ""
        yas.value = ""
        banyo.value = ""
        page.update()

    page.add(
        oda, salon, banyo, brut, net, yas, ft.Row(controls=[ddtext, dd, ft.ElevatedButton("Fiyat Tahmin Et", on_click=btn_click), greetings]),
    )

ft.app(target=main)