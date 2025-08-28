
import time
import wifi
import socketpool
import adafruit_requests

class Adhyay1_WiFi:
    def __init__(self, ssid, password):
        """Initialize WiFi connection"""
        self.ssid = ssid
        self.password = password
        self.connected = False
        self._connect()
    
    def _connect(self):
        """Internal connection handler"""
        try:
            wifi.radio.connect(self.ssid, self.password)
            self.pool = socketpool.SocketPool(wifi.radio)
            self.requests = adafruit_requests.Session(self.pool)
            self.connected = True
            time.sleep(1)  # Stabilization delay
        except Exception as e:
            print("WiFi Error:", e)
            self.connected = False
    
    def read(self, url, timeout=5):
        """HTTP GET request (similar to Bluetooth read)"""
        if not self.connected:
            self._connect()
            if not self.connected:
                return None
        
        try:
            response = self.requests.get(url, timeout=timeout)
            return response.text
        except Exception as e:
            print("Read Error:", e)
            return None
    
    def write(self, url, data=None):
        """HTTP POST request (similar to Bluetooth write)"""
        if not self.connected:
            self._connect()
            if not self.connected:
                return False
        
        try:
            response = self.requests.post(url, data=data)
            return response.status_code == 200
        except Exception as e:
            print("Write Error:", e)
            return False
    
    def is_connected(self):
        """Check connection status"""
        return self.connected