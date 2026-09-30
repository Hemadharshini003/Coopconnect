import 'package:flutter/material.dart';

class SyncCentreScreen extends StatefulWidget {
  const SyncCentreScreen({Key? key}) : super(key: key);

  @override
  State<SyncCentreScreen> createState() => _SyncCentreScreenState();
}

class _SyncCentreScreenState extends State<SyncCentreScreen> {
  bool _isSyncing = false;
  String _syncStatus = 'Synced';

  void _triggerSync() {
    setState(() {
      _isSyncing = true;
    });

    Future.delayed(const Duration(seconds: 2), () {
      setState(() {
        _isSyncing = false;
        _syncStatus = 'All 1 Pending Operations Synced Successfully';
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Offline Sync Centre'),
        backgroundColor: const Color(0xFF0F5A47),
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Card(
              child: ListTile(
                leading: Icon(_isSyncing ? Icons.sync : Icons.cloud_done, color: const Color(0xFF0F5A47)),
                title: Text(_syncStatus, style: const TextStyle(fontWeight: FontWeight.bold)),
                subtitle: const Text('Last synced: Just now'),
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton.icon(
              onPressed: _isSyncing ? null : _triggerSync,
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFFD97706),
                foregroundColor: Colors.white,
                minimumSize: const Size.fromHeight(50),
              ),
              icon: const Icon(Icons.refresh),
              label: Text(_isSyncing ? 'Synchronizing with Server...' : 'SYNCHRONIZE NOW'),
            ),
          ],
        ),
      ),
    );
  }
}
