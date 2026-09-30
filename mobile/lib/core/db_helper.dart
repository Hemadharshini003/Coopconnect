import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import 'constants.dart';

class DbHelper {
  static Database? _db;

  static Future<Database> get database async {
    if (_db != null) return _db!;
    _db = await _initDatabase();
    return _db!;
  }

  static Future<Database> _initDatabase() async {
    final path = join(await getDatabasesPath(), AppConstants.dbName);
    return await openDatabase(
      path,
      version: AppConstants.dbVersion,
      onCreate: (db, version) async {
        // 1. cached_user
        await db.execute('''
          CREATE TABLE cached_user (
            id TEXT PRIMARY KEY,
            email TEXT,
            full_name TEXT,
            role TEXT,
            preferred_language TEXT,
            cooperative_id TEXT
          )
        ''');

        // 2. cached_member_profile
        await db.execute('''
          CREATE TABLE cached_member_profile (
            id TEXT PRIMARY KEY,
            membership_number TEXT,
            education_level TEXT,
            occupation TEXT,
            years_of_experience INTEGER,
            profile_completion_percentage REAL
          )
        ''');

        // 3. cached_skills
        await db.execute('''
          CREATE TABLE cached_skills (
            id TEXT PRIMARY KEY,
            name TEXT,
            code TEXT,
            category TEXT,
            current_level INTEGER
          )
        ''');

        // 4. cached_courses
        await db.execute('''
          CREATE TABLE cached_courses (
            id TEXT PRIMARY KEY,
            title TEXT,
            description TEXT,
            category TEXT,
            duration_minutes INTEGER
          )
        ''');

        // 5. cached_lessons
        await db.execute('''
          CREATE TABLE cached_lessons (
            id TEXT PRIMARY KEY,
            course_id TEXT,
            title TEXT,
            text_content TEXT,
            sequence_number INTEGER
          )
        ''');

        // 6. cached_quizzes
        await db.execute('''
          CREATE TABLE cached_quizzes (
            id TEXT PRIMARY KEY,
            course_id TEXT,
            title TEXT,
            questions_json TEXT
          )
        ''');

        // 7. cached_opportunities
        await db.execute('''
          CREATE TABLE cached_opportunities (
            id TEXT PRIMARY KEY,
            title TEXT,
            description TEXT,
            location TEXT,
            stipend_or_salary TEXT
          )
        ''');

        // 8. cached_applications
        await db.execute('''
          CREATE TABLE cached_applications (
            id TEXT PRIMARY KEY,
            opportunity_id TEXT,
            status TEXT,
            applied_at TEXT
          )
        ''');

        // 9. pending_sync_operations
        await db.execute('''
          CREATE TABLE pending_sync_operations (
            id TEXT PRIMARY KEY,
            entity_type TEXT,
            entity_id TEXT,
            operation TEXT,
            payload_json TEXT,
            created_at TEXT
          )
        ''');

        // 10. sync_metadata
        await db.execute('''
          CREATE TABLE sync_metadata (
            key TEXT PRIMARY KEY,
            value TEXT
          )
        ''');
      },
    );
  }
}
