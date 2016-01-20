from Tkinter import *
from ttk import Frame, Button, Style
import tkFileDialog
import csv
from geopy.geocoders import GoogleV3
geolocator = GoogleV3(api_key='AIzaSyC5OTY3EcpttVbHMhs5PTNj2YSYFbNtiSw') #using server api key @ https://console.developers.google.com/apis/api/geocoding_backend/usage?project=tough-talent-110721&duration=PT1H

#global
Master ={}
outputFile =''
success = 'Failure'

class Application(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Batch Geocoder")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.place(x=50, y=50)
        
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        
        scrollbar = Scrollbar(self)
        scrollbar.pack( side = RIGHT, fill=Y)
        
		
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Run", command=self.onOpen)
        fileMenu.add_command(label="Exit", underline=0, command=self.onExit)
        
        menubar.add_cascade(label="File", menu=fileMenu)
        #menubar.add_command(label="Run", command=self.runScript)
        
        self.txt = Text(self, yscrollcommand = scrollbar.set)
        scrollbar.config( command = self.txt.yview )
        self.txt.pack(fill=BOTH, expand=1)


    def onOpen(self):
      
        ftypes = [('CSV Files', '*.csv'), ('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes, title='Select file to be geocoded')
        fl = dlg.show()
        self.openSecondFile(fl)
##        if fl != '':
##            text = self.openSecondFile(fl)
##            
##            self.txt.insert(END, text)
            
    def openSecondFile(self, filename):
        #print self, filename
        ftypes = [('CSV Files', '*.csv'), ('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes, title='Select your library key file')
        fl = dlg.show()
        self.readFile(fl, filename)
##        if fl != '':
##            text = self.readFile(fl,filename)
##            #print text
##            self.txt.insert(END, text)
			
    def onExit(self):
        self.quit()

    ## Begin Script
    def readFile(self, filename1, filename2):
        print "Input 1: ", filename2
        print "Input 2: ", filename1
        outputFile = filename2.strip('.csv') + '__geocoded.csv'

        with open(filename2, 'rb') as database:
            with open(filename1, 'rb') as librarykey:
                header = [h.strip() for h in database.next().split(',')]
                #print header
                print "running..."
                print
                try:
          
                    LegacyReader = csv.DictReader(database, delimiter=',', fieldnames=header)
                    LibraryReader = csv.DictReader(librarykey, delimiter=',')
                    
                    for rows in LegacyReader:
                        #print rows
                        #print rows['field_program_location']
                        librarylist = rows['field_program_location'].split(' | ')

                        Master[rows['field_custom_id']]= []               
                        
                        templist = [s for s in librarylist if ',' in s]
                        for fulladdresses in templist:
                            try:
                                #Link Site Libraries
                                #print rows['field_custom_id'], "LINK Site: ",fulladdresses
                                geolocation = geolocator.geocode(fulladdresses, timeout=10, bounds=[43.23,-97.62,49.57, -89.33])
                                geocodelatitude = geolocation.latitude
                                geocodelongitude = geolocation.longitude
                                LatLong = str(geocodelatitude) + '|' + str(geocodelongitude)
                                Master[rows['field_custom_id']].append(LatLong)
                                
                                if fulladdresses in librarylist:
                                    librarylist.remove(fulladdresses)
                            except Exception as inst:
                                print 'Geocoding error at ' + fulladdresses + ': '
                                print type(inst)
                                print inst.args


                        #Libraries        
                        for libraries in librarylist:
                            #print rows['field_custom_id'], "Library: ", libraries
                            Master[rows['field_custom_id']].append(libraries.upper())

                    #print Master
                    LibraryMaster = {}
                    for rows in LibraryReader:
                        #print rows
                        LibraryMaster[rows['Location']]= []
                        LibraryMaster[rows['Location']].append(rows['field_lat_long'])

                    def DictionaryCompare():
                        for key, value in Master.iteritems():
                            for values in value:
                                if values in LibraryMaster.keys():
                                    temp = values
                                    Master[key].remove(temp)
                                    Master[key].append(''.join(LibraryMaster[values]))
                                else:
                                    values = values


                    for key, value in Master.iteritems():
                        for values in value:
                            if values in LibraryMaster.keys():
                                DictionaryCompare()
                                continue
                            else:
                                 pass

##                    saveas()
                    
                    with open(outputFile, 'w') as csvoutput:
                        fieldnames = ['Location', 'field_lat_long']
                        writer = csv.DictWriter(csvoutput, fieldnames=fieldnames, extrasaction='ignore', lineterminator='\n')
                        writer.writeheader()
                        for key, value in sorted(Master.items()):                                 
                                stringvalue = '^'.join(value)
                                writer.writerow({'Location': key, 'field_lat_long': stringvalue})
                                #print('Location: ',key, 'field_lat_long', stringvalue)
								
                        print


                        print 'Success! Your file is located at ', outputFile		
                    
                
                except:
                    return str("Something failed - Make sure the file you selected contains the rows: 'field_program_location' and 'field_custom_id'")

        return success

def main():
  
    root = Tk()
    ex = Application(root)
    #save = saveas(root)
    root.geometry("500x250+300+300")
    root.mainloop()
    root.destroy()


if __name__ == '__main__':
    main()
