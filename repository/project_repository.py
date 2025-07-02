from supabase import create_client, Client
from config import SUPABASE_ANON_KEY, SUPABASE_URL

class ProjectRepository:
    def __init__(self, project_id):
        self.project_id = project_id
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        self.table_name = "projects"

    def get_project_info(self):
        res = self.supabase.table(self.table_name).select("*").eq("id", self.project_id).single().execute()
        return res

    def add_charge(self, amount):
        # 현재 charge 값을 읽어옴
        res = self.get_project_info()
        if not hasattr(res, 'data') or not res.data or 'charge' not in res.data:
            raise ValueError('해당 프로젝트에 charge 필드가 없습니다.')
        current_charge = res.data['charge'] or 0
        new_charge = current_charge + amount
        update_res = self.supabase.table(self.table_name).update({"charge": new_charge}).eq("id", self.project_id).execute()
        return update_res