def query_select_users(username, password):
  return f"""
    select 
      username,
      password,
      nombre
      from production_stage_energas.users
      where username = '{username}'
      and password = '{password}';
    """