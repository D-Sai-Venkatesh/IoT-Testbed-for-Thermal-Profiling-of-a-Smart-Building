#include<dht.h>
#include<time.h>
dht DHT;
#define DHT11_pin 7

char id[3]={'0','0','5'};
char temp[8];
char rpi_id1 = '9';
char rpi_id2 = '9';
int connect_rpi = 0;
int no_ack_cnt = 0;
int ack_wait = 0;
long int start_time = millis();
long int wait_time = 60000;
int chk;
float temperature;
int first_touch = 0;
long int prev = millis();
int reset = 6;

void setup() {
  // put your setup code here, to run once:
  digitalWrite(reset,HIGH);
  Serial.begin(9600);
  delay(500);
  pinMode(reset,OUTPUT);
  digitalWrite(reset,HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(no_ack_cnt >=20)
  {
    delay(100);
//    digitalWri/te(reset,LOW);
    delay(500);
    defaulter();
  }
  read_code(temp);
  int process_num; 
  process_num = filter_code(temp);
  processor(process_num);
  if(millis() - prev >=1000)
  {
    prev = millis();
    Serial.println(wait_time);
    Serial.println(millis());
    Serial.print(temp[0]);
    Serial.print(temp[1]);
    Serial.print(temp[2]);
    Serial.print(temp[3]);
    Serial.print(temp[4]);
    Serial.print(temp[5]);
    Serial.print(temp[6]);
    Serial.print(temp[7]);
    Serial.println();   
  }
  if(millis() > wait_time)
  {
    Serial.println("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx");
    delay(100);
//    digitalWrite(reset,LOW);
    delay(500);
    defaulter();
  }
}

void read_code(char *temp)
{
  long int start_time_read = millis();
  long int end_time_read = start_time_read + 10000;
  int i1=0;
  while(i1 < 8)
  {
    if(Serial.available())
    {
      char temp_1 = (char)Serial.read();
      if( temp_1 == 'h' || temp_1 == 'a' || temp_1 == 's' || temp_1 == 'f')
      {
        temp[0] = temp_1;
        i1++;
        while(i1< 8)
        {
          if(Serial.available())
          {
           temp[i1] = (char)Serial.read();
            i1++; 
          }
          
        }
        break;
      }
    }
  }
}

void defaulter()
{
  rpi_id1 = '9';
  rpi_id2 = '9';
  connect_rpi = 0;
  no_ack_cnt = 0;
  ack_wait = 0;
  first_touch = 0;
  wait_time = millis() + 60000;
}

int filter_code(char* temp)
{
  if(temp[0]=='h' && temp[1]== 'i' && temp[2] == ' ' && temp[3] == ' ' && temp[4]== ' ' && temp[5] == ' ')
  {
    if(connect_rpi == 0)
    {
      rpi_id1 = temp[6];
      rpi_id2 = temp[7];
      return 1;
    }
  }
  else if(temp[0]=='h' && temp[1]== ' ' && temp[2] == id[0] && temp[3] == id[1] && temp[4]== id[2] && temp[5] == ' ' && temp[6] == rpi_id1 && temp[7] == rpi_id2)
  {
    connect_rpi = 1;
    first_touch=1;
    return 2;
  }
  else if(temp[0]=='s' && temp[1]== ' ' && temp[2] == id[0] && temp[3] == id[1] && temp[4]== id[2] && temp[5] == ' ' && temp[6] == rpi_id1 && temp[7] == rpi_id2)
  {
    if(ack_wait == 1)
    {
      no_ack_cnt++;
    }
    ack_wait = 1;   
    wait_time = millis()+ 60000;
    Serial.println("Send data  ");
    print_data(rpi_id1, rpi_id2);
    return 3;
  }
  else if(temp[0]=='a' && temp[1]== ' ' && temp[2] == id[0] && temp[3] == id[1] && temp[4]== id[2] && temp[5] == ' ' && temp[6] == rpi_id1 && temp[7] == rpi_id2)
  {
    no_ack_cnt = 0;
    wait_time = millis()+ 60000;
    ack_wait = 0;
    return 4;
  }
  else if(temp[0]=='f' && temp[1]== ' ' && temp[2] == id[0] && temp[3] == id[1] && temp[4]== id[2] && temp[5] == ' ' && temp[6] == rpi_id1 && temp[7] == rpi_id2)
  {
    delay(100);
//    digitalWrite(reset,LOW);
    delay(500);
    defaulter();
    return 5;
  }
  else
  {
    return 0;
  } 
  
}

void processor(int process)
{
  if(process == 1 && first_touch == 0)
  {
    Serial.print("hello ");
    Serial.print(id[0]);
    Serial.print(id[1]);
    Serial.print(id[2]);
    Serial.print(" r");
    Serial.print(rpi_id1);
    Serial.print(rpi_id2);
    Serial.print('\n');
  }
  //if we wnat to add additional processing we can add here 
  else if(process == 2)
  {

  }

  else if(process == 3)
  {
    //print_data(rpi_id1, rpi_id2);
  }

  else if(process == 4)
  {

  }

  else if(process == 5)
  {

  }
  
}

void print_data (char id1,char id2)
{
      delay(200);
      chk = DHT.read11(DHT11_pin);
      delay(200);
      temperature = DHT.temperature;
      
      Serial.print("data ");
      Serial.print(id[0]);
      Serial.print(id[1]);
      Serial.print(id[2]);
      Serial.print(" r");
      Serial.print(id1);
      Serial.print(id2);
      Serial.print(" ");
      Serial.print(id[0]);
      Serial.print(id[1]);
      Serial.print(id[2]);
      Serial.print(" ");
      Serial.print(temperature);
      Serial.print("\n");
}
