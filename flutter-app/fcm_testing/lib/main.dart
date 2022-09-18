import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/material.dart';
import  'package:intl/intl.dart';
import 'package:http/http.dart' as http;

import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:fcm_testing/services/local_notifications.dart';

Future<void> backroundHandler(RemoteMessage message) async {
  print("This is message from background");
  print(message.notification!.title);
  print(message.notification!.body);
}

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  FirebaseMessaging.onBackgroundMessage(backroundHandler);
  final fcmToken = await FirebaseMessaging.instance.getToken();
  print(fcmToken);
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: HomePage(),
    );
  }
}

class NotifPage extends StatefulWidget {
  final String company_email;
  final String company_name;
  const NotifPage(this.company_email, this.company_name);

  @override
  NotifPageState createState() => NotifPageState();
}

class NotifPageState extends State<NotifPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Container(
          child: Column(
            //mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Center(
                  child: Padding(
                      padding: EdgeInsets.only(top: 20.0),
                      child: ClipOval(
                        child: Image.asset(
                          'assets/imgs/test.png',
                          height: 180,
                          width: 180,
                        ),
                      )
                  )
              ),
              const Text('Enterprise Access Request:  ',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                      color: Colors.black,
                      fontSize: 17,
                      fontWeight: FontWeight.bold
                  )
              ),
              SizedBox(height: 20),
              Icon(
                Icons.person,
                size: 25,
              ),
              SizedBox(height: 5),
              Text(widget.company_email,
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: Colors.grey,
                    fontSize: 14,
                  )
              ),
              SizedBox(height: 25),
              Icon(
                Icons.access_time,
                size: 25,
              ),
              SizedBox(height: 5),
              Text(DateFormat("hh:mm:ss a").format(DateTime.now()),
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: Colors.grey,
                    fontSize: 14,
                  )
              ),
              SizedBox(height: 3),
              Text(DateFormat("MMMM, dd, yyyy").format(DateTime.now()),
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: Colors.grey,
                    fontSize: 14,
                  )
              ),
              SizedBox(height: 28),
              Icon(
                Icons.business,
                size: 25,
              ),
              Text(widget.company_name,
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: Colors.grey,
                    fontSize: 14,
                  )
              ),
              SizedBox(height: 28),
              Icon(
                Icons.location_on,
                size: 25,
              ),
              Text('68.132.47.130',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: Colors.grey,
                    fontSize: 14,
                  )
              ),
              SizedBox(height: 3),
              Text('Huntington, New York, US',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: Colors.grey,
                    fontSize: 14,
                  )
              ),
              SizedBox(height: 30),
              Center(
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: <Widget>[
                    Padding(
                        padding: EdgeInsets.only(left: 0.0),
                        child: OutlinedButton.icon(
                            onPressed: () {
                              var url = Uri.parse('http://10.33.133.20:8000/apiv1/trust_enterprise/');
                              http.post(url, body: {
                                'company_name': widget.company_name,
                                'auth_user_uid': 'roM8dQofqKsyA2Y5wOf0hDJT66wRQhlQ',
                                'verdict': 'YES',
                              });
                              print("sent");
                              Navigator.pop(context);
                            },
                            style: ButtonStyle(
                              foregroundColor: MaterialStateProperty.all(Colors.green),
                            ),
                            icon: Icon(Icons.check, size: 25),
                            label: Text('Trust')),
                    ),
                    Padding(
                      padding: EdgeInsets.only(left: 0.0),
                      child: OutlinedButton.icon(
                          onPressed: () {
                            var url = Uri.parse('http://10.33.133.20:8000/apiv1/trust_enterprise/');
                            http.post(url, body: {
                              'company_name': widget.company_name,
                              'auth_user_uid': 'roM8dQofqKsyA2Y5wOf0hDJT66wRQhlQ',
                              'verdict': 'NO',
                            });
                            print("sent");
                            Navigator.pop(context);
                          },
                          style: ButtonStyle(
                            foregroundColor: MaterialStateProperty.all(Colors.red),
                          ),
                          icon: Icon(Icons.clear, size: 25),
                          label: Text('Do Not Trust')),
                    ),
                  ],
                ),
              ),
              SizedBox(height: 10),
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                  // Respond to button press
                },
                child: Text("(Go back)"),
              )
              // Padding(
              //     padding: EdgeInsets.only(left: 55.0, right: 55.0),
              //     child: ElevatedButton(
              //       style: ButtonStyle(
              //         //backgroundColor: MaterialStateProperty.all(Colors.blue),
              //           foregroundColor: MaterialStateProperty.all(Colors.black)
              //       ),
              //       onPressed: null,
              //       child: Text(
              //           'View Old Requests'
              //       ),
              //     )
              // )
            ],
          ),
        )
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String notificationMsg = "Waiting for notifications";
  @override
  void initState() {
    // TODO: implement initState
    super.initState();

    FirebaseMessaging.onMessage.listen((RemoteMessage message) {
      setState(() {
        print('Got a message whilst in the foreground!');
        print('Message data: ${message.data}');

        if (message.notification != null) {
          print('Message also contained a notification: ${message.notification}');
        }

        print(message.data['company_email']);
        print(message.data['company_name']);
        Navigator.of(context).push(MaterialPageRoute(builder: (context) => NotifPage(message.data['company_email'], message.data['company_name'])));
      });
      // Navigator.push(
      //   context,
      //   MaterialPageRoute(builder: (context) => const NotifState()),
      // );
    });
    // Foregrand State
    FirebaseMessaging.onMessage.listen((event) {
      LocalNotificationService.showNotificationOnForeground(event);
      setState(() {
        notificationMsg =
        "${event.notification!.title} ${event.notification!.body}";
      });
    });

    // background State
    // FirebaseMessaging.onMessageOpenedApp.listen((event) {
    //   setState(() {
    //     notificationMsg =
    //     "${event.notification!.title} ${event.notification!.body} I am coming from background";
    //   });
    // });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Container(
          child: Column(
            //mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Center(
                  child: Padding(
                      padding: EdgeInsets.only(top: 70.0),
                      child: ClipOval(
                        child: Image.asset(
                          'assets/imgs/test.png',
                          height: 280,
                          width: 280,
                        ),
                      )
                  )
              ),
              const Text('Welcome to ANS Verification ',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                      color: Colors.black,
                      fontSize: 16,
                      fontWeight: FontWeight.bold
                  )
              ),
              SizedBox(height: 20),
              const Padding(
                padding: EdgeInsets.only(left: 60.0, right: 60.0),
                child: Text("ANS Verify helps you maintain your trusted organizations. You'll use this "
                    "app to approve/trust various enterprises accessing your address.",
                    textAlign: TextAlign.center,
                    style: TextStyle(
                        color: Colors.grey,
                        fontSize: 14,
                        height: 1.5
                    )
                ),
              ),
              SizedBox(height: 55),
              Padding(
                  padding: EdgeInsets.only(left: 60.0, right: 60.0),
                  child: OutlinedButton(
                    style: ButtonStyle(
                      //backgroundColor: MaterialStateProperty.all(Colors.blue),
                        foregroundColor: MaterialStateProperty.all(Colors.black)
                    ),
                    onPressed: () {} ,
                    child: Text(
                        'View Old Requests'
                    ),
                  )
              )
            ],
          ),
        )
    );
  }
}