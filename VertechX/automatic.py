import threading
import time

class AutoMode:
    def __init__(self):
        self.active = False
        self.thread = None

    def start(self):
        if not self.active:
            self.active = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()
            print("✅ Auto Mode Started")

            
    def stop(self):
        self.active = False
        print("❌ Auto Mode Stopped")

    def run(self):
        while self.active:
            count = 100 
            while count > 0 and self.active :
                print(f"Count = {count}")
                
                if count == 90 :
                    #turn on valve1
                    pass
                elif count == 80 :
                    #turn on valve2 & valve3 and turn off valve1
                    pass
                elif count == 70 :
                    #turn off valve3 & valve2 and turn on leds
                    pass
                elif count == 60 :
                    #turn on pump1 & pump2 
                    pass
                     
                count-=1
                time.sleep(2)

           
