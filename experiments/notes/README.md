# 一、数据可视化

# 二、数据特征

### 1.features的数据类型分为两类

##### 布尔

```
'users_3w',
'twolow_users', 
'roam_users02', 
'roam_users01',
'vv_type',
'in16_roam_tag'
```

##### 数值

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

### 2.Imbalanced data

##### 总体情况

label==0 : 299335

label==1: 221

label ==1 vs all : 0.0007 vs 1

##### 解决办法

- under sampling
- over sampling
- cost sensitive
- anomaly detection
- 如图

![1581688337158](/home/toorevitimirp/Desktop/手机用户分类模型/App/phone-users-prober/experiments/notes/image/1581688337158.png)

### 3.对于数值型特征，数据在低处十分密集。正类、负类的分布差别很小。

### 4.布尔型特征分布情况如下。对于所有特征，特征值为0的比例非常高。正类、负类的分布差别很小。

```
				users_3w      
label       	0     1             
0         251796  47539
1            214      7
############################
				twolow_users       
label              0      1        
0             279117  20218
1                214      7
############################
				roam_users02       
label              0     1       
0             294261  5074
1                197    24
############################
				roam_users01       
label              0      1        
0             288157  11178
1                186     35
############################
				vv_type       
label         0      1        
0        259488  39847
1           196     25
############################
				in16_roam_tag      
label                0      1        
0              276510  22825
1                 217      4
############################
```

# 三、降维

### 特征选择

###### 1.移除低方差特征

移除那些在整个数据集中特征值为0或者为1的比例超过80%的特征后，只剩下数值型特征。



### 特征提取

###### 1. PCA

保留99%的variance的情况下，数据可以降到3维

![1582359911314](/home/toorevitimirp/Desktop/手机用户分类模型/App/phone-users-prober/experiments/notes/image/1582359911314.png)

![1582359949607](/home/toorevitimirp/Desktop/手机用户分类模型/App/phone-users-prober/experiments/notes/image/1582359949607.png)

![1582360010849](/home/toorevitimirp/Desktop/手机用户分类模型/App/phone-users-prober/experiments/notes/image/1582360010849.png)

# 四、处理imbalanced data



# 五、模型

###  SVM

### 不考虑skewed class问题，直接训练

![1581924881240](/home/toorevitimirp/Desktop/手机用户分类模型/App/phone-users-prober/experiments/notes/image/1581924334184.png)

### cost learning

class_weight={0: 7, 1: 10000}

![1582015111861](/home/toorevitimirp/Desktop/手机用户分类模型/App/phone-users-prober/experiments/notes/image/1582015111861.png)