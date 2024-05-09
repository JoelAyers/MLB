import PySimpleGUI as sg

for i in range(0,5000):
    sg.one_line_progress_meter("Meter", i, 5000)