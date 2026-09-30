import { openDB, DBSchema, IDBPDatabase } from 'idb';

interface CoopConnectDB extends DBSchema {
  cached_courses: {
    key: string;
    value: any;
  };
  cached_assessments: {
    key: string;
    value: any;
  };
  cached_opportunities: {
    key: string;
    value: any;
  };
  pending_sync_queue: {
    key: string;
    value: {
      id: string;
      type: string;
      payload: any;
      timestamp: string;
    };
  };
}

let dbPromise: Promise<IDBPDatabase<CoopConnectDB>> | null = null;

const getDB = () => {
  if (!dbPromise) {
    dbPromise = openDB<CoopConnectDB>('coopconnect_offline_db', 1, {
      upgrade(db) {
        if (!db.objectStoreNames.contains('cached_courses')) {
          db.createObjectStore('cached_courses', { keyPath: 'id' });
        }
        if (!db.objectStoreNames.contains('cached_assessments')) {
          db.createObjectStore('cached_assessments', { keyPath: 'id' });
        }
        if (!db.objectStoreNames.contains('cached_opportunities')) {
          db.createObjectStore('cached_opportunities', { keyPath: 'id' });
        }
        if (!db.objectStoreNames.contains('pending_sync_queue')) {
          db.createObjectStore('pending_sync_queue', { keyPath: 'id' });
        }
      },
    });
  }
  return dbPromise;
};

export const saveOfflineCourse = async (course: any) => {
  const db = await getDB();
  await db.put('cached_courses', course);
};

export const getOfflineCourses = async () => {
  const db = await getDB();
  return await db.getAll('cached_courses');
};

export const enqueueOfflineAction = async (type: string, payload: any) => {
  const db = await getDB();
  const item = {
    id: `sync_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
    type,
    payload,
    timestamp: new Date().toISOString()
  };
  await db.put('pending_sync_queue', item);
  return item;
};

export const getPendingSyncQueue = async () => {
  const db = await getDB();
  return await db.getAll('pending_sync_queue');
};

export const clearSyncQueue = async () => {
  const db = await getDB();
  await db.clear('pending_sync_queue');
};
