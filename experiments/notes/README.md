# features的数据类型

### 布尔

```
'users_3w',
'twolow_users', 
'roam_users02', 
'roam_users01',
'vv_type',
'in16_roam_tag'
```

### 数值

```
'roam_call_duration',
'roam_duration_02',
'mon_use_days',
'is_p_app_wx_times', 
'zhujiao_time', 
'zhujiao_times',
'mb5',
'mb10',
'mb30', 
'mb60', 
'ma60', 
'total_count',
'beijiao_times', 
'use_days', 
'zhujiao', 
'beijiao',
'zhujiao_jt', 
'open', 
'close', 
'open_day', 
'cell_num'
```

# Imbalanced data

### 总体情况

label==0 : 299335

label==1: 221

label ==1 / all = 0.0007

### label关于布尔型features的分布

```
users_3w       0      1
label                  
0         251796  47539
1            214      7
############################
twolow_users       0      1
label                      
0             279117  20218
1                214      7
############################
roam_users02       0     1
label                     
0             294261  5074
1                197    24
############################
roam_users01       0      1
label                      
0             288157  11178
1                186     35
############################
vv_type       0      1
label                 
0        259488  39847
1           196     25
############################
in16_roam_tag       0      1
label                       
0              276510  22825
1                 217      4
############################
```