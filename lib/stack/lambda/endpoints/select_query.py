def query_select_users(username, password):
  return f"""
    select distinct
      dni,
      nombre as name
      from production_raw_iot_advizo.users
      where username = '{username}'
      and password = '{password}'
    ;
    """