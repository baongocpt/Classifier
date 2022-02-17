# -*- coding: utf-8 -*-
from tkinter import Tk, Label, Button, filedialog
from tkinter import *
from tkinter.ttk import Progressbar
import tkMessageBox
import os
import shutil
import subprocess
import pandas as pd
from geopy.geocoders import Nominatim
from datetime import datetime


class Classifier:
    def __init__(self, master):
        self.master = master
        master.title("Classify photos and videos")

        self.indir = StringVar()
        # self.indir.set(os.getcwd())
        self.indir.set(os.path.join(os.getcwd(),"photos"))
        self.indir.set("E:/Photos/New DCIM/101APPLE")
        self.outdir = StringVar()
        # self.outdir.set(os.getcwd())
        self.outdir.set(os.path.join(os.getcwd(), "output"))
        self.outdir.set("E:/2. Photos/Test")

        self.label_indir = Label(master, text="Source Folder :")
        self.label_outdir = Label(master, text="Destination Folder :")
        self.entry_indir = Entry(master, textvariable=self.indir, width=45)
        self.entry_outdir = Entry(master, textvariable=self.outdir, width=45)
        self.button_inbrowse = Button(
            text="Browse",
            command=lambda: self.indir.set(filedialog.askdirectory()))
        self.button_outbrowse = Button(
            text="Browse",
            command=lambda: self.outdir.set(filedialog.askdirectory()))

        self.label_indir.grid(row=0, column=0, sticky=W)
        self.label_outdir.grid(row=1, column=0, sticky=W)
        self.entry_indir.grid(row=0, column=1)
        self.entry_outdir.grid(row=1, column=1)
        self.button_inbrowse.grid(row=0, column=2, padx=5)
        self.button_outbrowse.grid(row=1, column=2, padx=5)

        self.button_execute = Button(text="Execute", command=self.execute)
        self.button_open_outdir = Button(
            text="Open Output Folder", command=self.open_outdir)
        self.close_button = Button(master, text="Close", command=master.destroy)

        self.button_execute.grid(row=3, column=1, pady=5)
        self.button_open_outdir.grid(row=3, column=0, pady=5)
        self.close_button.grid(row=3, column=2, pady=5)

        self.progress = Progressbar(orient=HORIZONTAL, length=100, mode='determinate')

    def open_outdir(self):
        os.system("explorer \"%s\"" % os.path.normpath(self.outdir.get()))

    def execute(self):
        if not os.path.exists(self.outdir.get()):
            self.popupmsg("Output directory does not exist")
            return None
        logs = {
            'src_files': [],
            'dst_files': [],
            'coordinate': [],
            'country': [],
            'county': [],
            'suburb': [],
            'city': [],
            'town': [],
            'created_date': []
        }
        files = self.list_media_files(self.indir.get())
        if files:
            self.progress.grid(row=4, column=1)
        for file in files:
            print(file)
            if file.endswith('.AAE'):
                continue
            lat, lat_dir, lon, lon_dir = self.get_coordinate(file)
            logs['src_files'].append(file)
            year, month, date = self.get_create_date(file)
            logs['created_date'].append(date)
            if lat and lat_dir and lon and lon_dir:
                address_info = self.get_position(lat, lat_dir, lon, lon_dir)
                _address = address_info.get('country')
                if _address:
                    _address = _address.encode('utf-8', 'ignore').decode('utf-8')
                _county = address_info.get('county')
                if _county:
                    _county = _county.encode('utf-8', 'ignore').decode('utf-8')
                _suburb = address_info.get('suburb')
                if _suburb:
                    _suburb = _suburb.encode('utf-8', 'ignore').decode('utf-8')
                _city = address_info.get('city')
                if _city:
                    _city = _city.encode('utf-8', 'ignore').decode('utf-8')
                _town = address_info.get('town')
                if _town:
                    _town = _town.encode('utf-8', 'ignore').decode('utf-8')
                address_info['country'] = _address
                address_info['county'] = _county
                address_info['suburb'] = _suburb
                address_info['city'] = _city
                address_info['town'] = _town
                dst_file = self.move_file(file, year, month, date, address_info)
                AAE_file = os.path.join(
                    os.path.dirname(file),
                    os.path.splitext(os.path.basename(file))[0] + ".AAE")
                if os.path.exists(AAE_file):
                    self.move_file(AAE_file, year, month, date, address_info)
                logs['dst_files'].append(dst_file)
                logs['coordinate'].append("%s %s, %s %s" % (lat, lat_dir, lon, lon_dir))
                logs['country'].append(_address)
                logs['county'].append(_county)
                logs['suburb'].append(_suburb)
                logs['city'].append(_city)
                logs['town'].append(_town)
            else:
                dst_file = self.move_file(file, year, month, date)
                AAE_file = os.path.join(
                    os.path.dirname(file),
                    os.path.splitext(os.path.basename(file))[0] + ".AAE")
                if os.path.exists(AAE_file):
                    self.move_file(AAE_file, year, month, date)
                logs['dst_files'].append(dst_file)
                logs['coordinate'].append("N/A")
                logs['country'].append("N/A")
                logs['county'].append("N/A")
                logs['suburb'].append("N/A")
                logs['city'].append("N/A")
                logs['town'].append("N/A")
            percent = (float(files.index(file)+1) / float(len(files))) * 100
            self.progress['value'] = percent
            self.master.update_idletasks()
        df = pd.DataFrame(logs, columns=['src_files', 'dst_files',
                                         'coordinate', 'country',
                                         'county', 'suburb',
                                         'city', 'town', 'created_date'])
        # df.to_csv('logs.csv', index=False, header=True, encoding='utf-8')
        df.to_excel('log.xls', index=False, header=True, encoding='utf-8')
        # self.progress.destroy()

    def list_media_files(self, path):
        media_files = []
        for path, subdirs, files in os.walk(path):
            for name in files:
                media_files.append(os.path.normpath(os.path.join(path, name)))
        return media_files

    def get_coordinate(self, file):
        try:
            _cmd = "exiftool -c \"%.6f degrees\" \"" + file + "\""
            result = subprocess.Popen(_cmd, shell=True,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
            output, error = result.communicate()
            _re = re.search(".*GPS Position\s+:\s(.*) degrees (.*), (.*) degrees (.*)", output)
            lat = _re.group(1)
            lat_dir = _re.group(2)
            lon = _re.group(3)
            lon_dir = _re.group(4)
            return lat, lat_dir, lon, lon_dir
        except Exception:
            return None, None, None, None

    def get_position(self, lat, lat_dir, lon, lon_dir):
        try:
            locator = Nominatim(user_agent="http")
            coordinates = "%s %s, %s %s" % (lat, lat_dir, lon, lon_dir)
            location = locator.reverse(coordinates)
            address = location.raw.get('address')
            # print address
            output_info = {'country': address.get('country'),
                           'county': address.get('county'),
                           'suburb': address.get('suburb'),
                           'city': address.get('city'),
                           'town': address.get('town'),
                           'state': address.get('state')}
            return output_info
        except Exception as msg:
            print(msg)

    def get_create_date(self, file):
        timestamp = os.path.getctime(file)
        date_time = datetime.fromtimestamp(timestamp)
        year = date_time.strftime("%Y")
        month = date_time.strftime("%B")
        date = date_time.strftime("%Y-%m-%d")
        return year, month, date

    def check_media_file(self, file, extension=None):
        media_files = ['.JPG', '.MOV', '.PNG', 'MP4']
        type = os.path.splitext(file)[-1]
        if extension.upper() == type.upper():
            return True
        if type.upper() in media_files:
            return True
        return False

    def move_file(self, file, year, month, date, address_info=None):
        if address_info:
            dst_file = os.path.normpath(
                os.path.join(
                    self.outdir.get(),
                    address_info['country']
                )
            )
            if not os.path.exists(dst_file):
                os.mkdir(dst_file)
            folder_1 = address_info['county'] or address_info['city']
            if address_info.get('state'):
                folder_1 = address_info.get('state')
            dst_file = os.path.join(dst_file, folder_1)
            if not os.path.exists(dst_file):
                os.mkdir(dst_file)
            folder_2 = address_info['suburb'] or address_info['town']
            if address_info.get('state'):
                folder_2 = address_info.get('county')
            dst_file = os.path.join(dst_file, folder_2)
            if not os.path.exists(dst_file):
                os.mkdir(dst_file)
        else:
            dst_file = os.path.normpath(
                os.path.join(
                    self.outdir.get(), 'Others'
                )
            )
            if not os.path.exists(dst_file):
                os.mkdir(dst_file)
        dst_file = os.path.join(dst_file, year)
        if not os.path.exists(dst_file):
            os.mkdir(dst_file)
        dst_file = os.path.join(dst_file, month)
        if not os.path.exists(dst_file):
            os.mkdir(dst_file)
        dst_file = os.path.join(dst_file, date)
        if not os.path.exists(dst_file):
            os.mkdir(dst_file)
        shutil.copy2(file, dst_file)
        return os.path.join(dst_file, os.path.basename(file))

    def popupmsg(self, msg):
        popup = Tk()
        popup.wm_title("!")
        label = Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        B1 = Button(popup, text="OK", command=popup.destroy)
        B1.pack()
        popup.mainloop()


if __name__ == '__main__':
    gui = Tk()
    # gui.iconbitmap("table_merge_cells_icon_135130.ico")
    gui.geometry("500x150")
    gui['bd'] = 10
    gui['relief'] = RAISED
    gui['borderwidth'] = 5
    gui['padx'] = 15
    gui['pady'] = 15
    Classifier(gui)
    gui.mainloop()
