import 'dart:convert';
import 'package:sqflite/sqflite.dart';
import 'db_helper.dart';

class SyncEngine {
  static Future<void> queueOperation({
    required String entityType,
    required String entityId,
    required String operation,
    required Map<String, dynamic> payload,
  }) async {
    final db = await DbHelper.database;
    final syncId = 'sync_${DateTime.now().millisecondsSinceEpoch}';
    
    await db.insert('pending_sync_operations', {
      'id': syncId,
      'entity_type': entityType,
      'entity_id': entityId,
      'operation': operation,
      'payload_json': jsonEncode(payload),
      'created_at': DateTime.now().toIso8601String(),
    });
  }

  static Future<List<Map<String, dynamic>>> getPendingQueue() async {
    final db = await DbHelper.database;
    return await db.query('pending_sync_operations');
  }

  static Future<void> clearQueue() async {
    final db = await DbHelper.database;
    await db.delete('pending_sync_operations');
  }
}
