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
      dni,
      map_id,
      url_map
      from production_raw_iot_advizo.map_factory
      where dni = '{dni}'
    ;
    """

def query_get_coordenates(dni,map_id):
  return f"""
    select distinct
      dni,
      map_id,
      sensor_id,
      coordenates
    from production_raw_iot_advizo.coordenates
    where dni = '{dni}' and map_id = '{map_id}'
    ;
    """