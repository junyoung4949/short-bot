from supabase import create_client, Client
from config import SUPABASE_ANON_KEY, SUPABASE_URL

class ItemRepository:
    def __init__(self, user_id, project_id):
        self.user_id = user_id
        self.project_id = project_id
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

        self.table_name = "json_items"

    def save_item(self, item):
        item["project_id"] = self.project_id
        res = self.supabase.table(self.table_name).insert(item).execute()
        return res

    def read_item(self, item_id):
        res = self.supabase.table(self.table_name).select("*").eq("id", item_id).single().execute()
        return res

    def read_item_random(self):
        res = self.supabase.table(self.table_name).select("*").eq("project_id", self.project_id).eq("status", "APPROVED").limit(1).execute()
        if res.data and len(res.data) > 0:
            return res.data[0]
        return None

    def update_item(self, item_id, new_item):
        res = self.supabase.table(self.table_name).update_item(item_id, new_item)
        return res

    def delete_item(self, item_id):
        self.supabase.table(self.table_name).delete().eq("id", item_id).execute()

    def update_status_uploaded(self, item_id):
        res = self.supabase.table(self.table_name).update({"status": "UPLOADED"}).eq("id", item_id).execute()
        return res