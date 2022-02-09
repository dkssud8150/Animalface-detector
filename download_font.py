import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# print(fm.findSystemFonts(fontpaths=None, fontext='ttf'))

# 한글 폰트 설정하기

fontpath = 'C:/Windows/Fonts/NanumGothicLight.ttf'
font = fm.FontProperties(fname=fontpath, size=10).get_name()
plt.rc('font', family=font)

