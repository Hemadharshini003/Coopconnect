import 'package:flutter/material.dart';
import 'sync_centre_screen.dart';

class MemberDashboardScreen extends StatelessWidget {
  const MemberDashboardScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Member Dashboard'),
        backgroundColor: const Color(0xFF0F5A47),
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.sync),
            onPressed: () {
              Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => const SyncCentreScreen()),
              );
            },
          )
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Card(
              color: const Color(0xFF0F5A47),
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text('Meena Jadhav', style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                    SizedBox(height: 4),
                    Text('Pragati Dairy Cooperative • Sinnar', style: TextStyle(color: Color(0xFFA7F3D0), fontSize: 12)),
                    SizedBox(height: 12),
                    Text('Role Readiness Score: 78.5%', style: TextStyle(color: Color(0xFFFDE047), fontSize: 16, fontWeight: FontWeight.bold)),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 20),
            const Text('AI Skill Gaps & Recommended Courses', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            Card(
              child: ListTile(
                leading: const Icon(Icons.warning, color: Colors.red),
                title: const Text('ERP Operation & Daily Entry'),
                subtitle: const Text('Required: Level 4 | Current: Level 1'),
                trailing: const Icon(Icons.chevron_right),
              ),
            ),
            Card(
              child: ListTile(
                leading: const Icon(Icons.book, color: Color(0xFF0F5A47)),
                title: const Text('ERP Fundamentals for Cooperative Staff'),
                subtitle: const Text('Duration: 90 Mins • Offline Ready'),
                trailing: const Icon(Icons.download_done, color: Colors.green),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
