from src.utilities.utils import execute_query


def update_roi_percentage(package_id: int, roi_percentage: float, admin_user_id: str):
    res = execute_query("call usp_update_roi_percentage(_package_id => %s, _percentage => %s, _admin_user_id => %s)",
                        (package_id, roi_percentage, admin_user_id))
    return res
