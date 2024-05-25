#include <SPI.h>
#include <Ethernet.h>
#include <P1AM.h>

bool messageSent = false;
byte mac[] = { 0x60, 0x52, 0xD0, 0x07, 0x7F, 0xCB };
IPAddress ip(192, 168, 1, 2);
EthernetServer server(10000);
String incomingData = ""; // String to store incoming data

void setup() {
  Serial.begin(115200);
  while(!Serial);
  while(!P1.init());
  Ethernet.begin(mac, ip);
  server.begin();

  Serial.println("Setup Complete");
}

void loop() {
  EthernetClient client = server.available();
  if (client) {
    Serial.println("Client connected.");
    while (client.connected()) {
      while (client.available()) {
        char c = client.read();
        incomingData += c; // Append the incoming character to the string

        // Check for a specific condition to process the string
        // For example, if you expect the client to send a newline at the end of the message:
        if (c == '\n') {
          Serial.println(incomingData); // Print the complete string

          if (!messageSent) {
            client.write("Hello PC");
            messageSent = true;
          }

          incomingData = ""; // Clear the string for the next message
        }
      }
    }
    client.stop();
    Serial.println("Client disconnected.");
    messageSent = false; // Reset the flag for the next client
  }
}
