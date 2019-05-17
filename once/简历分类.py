'''
简历分类
'''
import os
import shutil
import pandas as pd

src_dir = 'F:\\简历'
dst_root = 'F:\\分类简历'

def sort_by_experience(filename):
  '''
  根据经验分类
  '''
  if '1年' in  filename or '一年' in filename:
    return 1
  elif '2年' in filename or '二年' in  filename:
    return 2
  elif '3年' in  filename or '三年' in  filename:
    return 3
  elif '4年' in  filename or '四年' in filename:
    return 4
  elif '5年' in  filename or '五年' in filename:
    return 5
  else:
    return 0


df = pd.DataFrame(os.listdir(src_dir), columns=['filename'])
df['level'] = df.filename.apply(sort_by_experience)

for row in df.itertuples():
  print(row.filename, row.level)
  shutil.copy(os.path.join(src_dir, row.filename), os.path.join(dst_root, str(row.level)))
