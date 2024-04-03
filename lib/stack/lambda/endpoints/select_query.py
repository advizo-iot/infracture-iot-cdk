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

def query_get_map(dni):
  return f"""
    select distinct
      map_id,
      url_map,
      coordenates
      from production_raw_iot_advizo.map_factory
      where dni = '{dni}'
    ;
    """