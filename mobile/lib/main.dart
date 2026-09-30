import 'package:flutter/material.dart';
import 'screens/splash_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const CoopConnectApp());
}

class CoopConnectApp extends StatelessWidget {
  const CoopConnectApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CoopConnect AI',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primaryColor: const Color(0xFF0F5A47),
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF0F5A47),
          primary: const Color(0xFF0F5A47),
          secondary: const Color(0xFFD97706),
        ),
        useMaterial3: true,
      ),
      home: const SplashScreen(),
    );
  }
}
