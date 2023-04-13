import requests
import pandas as pd
from datetime import datetime
# -- sqlalchemy 2.x 는 오류남.
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String

# -- 경고 메시지 시끄러워서 끔
import warnings
warnings.filterwarnings(action='ignore')

health_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

pd.set_option("display.max_rows"        , None  )
pd.set_option("display.max_columns"     , None  )
pd.set_option("display.width"           , None  )
pd.set_option("display.max_colwidth"    , None  )

post_ip       = "192.168.0.157"
post_db       = "monitor_api"
post_id       = "airflow"
post_pw       = "airflow"
post_port     = "5432"

engine        = create_engine(f"postgresql://{post_id}:{post_pw}@{post_ip}/{post_db}", isolation_level="AUTOCOMMIT")

# ----------------------------------------------------------------
# ■ 01. REST API 로 상태정보를 READ 하여 Dataframe ( df_rest_api ) 으로 생성
# ----------------------------------------------------------------
# -- rest api 로 dag 의 상태 조회하여 (dag_id, is_active, is_paused 컬럼만 ) dataframe 으로 생성
req_cont_json  = requests.get("http://192.168.0.156:8080/api/v1/dags", auth=("airflow", "airflow")).json()
df_rest_api    = pd.DataFrame.from_dict(req_cont_json["dags"])[["dag_id","is_active","is_paused"]]
# -- dag_id 로 필터링 : af_col_ 로 시작되는 dag_id
df_rest_api    = df_rest_api.loc[df_rest_api["dag_id"].str.startswith("af_col_")]

# ----------------------------------------------------------------
# ■ 02. 생성된 dataframe 에 컬럼 추가
#     - status
#     - source_name
#     - health_time
# ----------------------------------------------------------------
# -- status 컬럼 추가
df_rest_api["status"      ] = df_rest_api.apply(lambda x : 
        'success'
        if x["is_active"] and (not x["is_paused"]) else 'failed'
    ,   axis=1
)
# -- source_name 컬럼 추가
df_rest_api["source_name" ] = df_rest_api.apply(lambda x :
        (str(x["dag_id"]).split('_')[2] + '_' + str(x["dag_id"]).split('_')[3]).upper()
        if len(str(x["dag_id"]).split('_')) >= 4 else ""
    ,   axis=1
)
# -- health_time 컬럼 추가
df_rest_api["health_time"] = health_time
# print(df_rest_api)

# ----------------------------------------------------------------
# ■ 03. 위 dataframe 을 Temp Table 로 DB 에 생성 ( 생성후 데이터 Insert )
# ----------------------------------------------------------------
# -- Temp 테이블 생성
meta = MetaData()
temptable_rest_api = Table(
        'df_rest_api'
    ,   meta
    ,   Column('dag_id'     , String)
    ,   Column('is_active'  , String)
    ,   Column('is_paused'  , String)
    ,   Column('status'     , String)
    ,   Column('source_name', String)
    ,   Column('health_time', String)
    ,   prefixes = ['TEMPORARY']
)
temptable_rest_api.create(engine)
# -- 데이터 Insert
df_rest_api.to_sql("df_rest_api", engine, if_exists='append', index=False)

# ----------------------------------------------------------------
# ■ 04. 위에서 Temp테이블로 생성된 dataframe 과 Postgres DB 안의 테이블을 Join 하여
#       health_checkup 에 insert
# ----------------------------------------------------------------
# -- 데이터 넣기 전에 truncate
# engine.execute("truncate table health_checkup")
# -- Dag 상태 정보 (temporary 테이블) 와 Dag 정보 (기존 테이블) 를 Join 하여 health check 정보 생성
engine.execute("""
insert into health_checkup (
      health_time
    , status
    , health_name
    , collect_channel
    , collect_group
    , collect_source
)
select to_timestamp(
           health_time
         , 'yyyy-mm-dd hh24:mi:ss'
       )                  as health_time
     , r.status           as status
     , g.code_name_kr     as health_name
     , s.collect_channel  as collect_channel
     , s.collect_group    as collect_group
     , s.collect_source   as collect_source
  from df_rest_api r
       join code_source s
         on s.source_name   = r.source_name
       join code_collect_group g
         on g.collect_group = s.collect_group
"""
)
# ----------------------------------------------------------------
# ■ 99. 연결 종료
# ----------------------------------------------------------------
engine.dispose()