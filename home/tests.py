from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

print(f'caminho: {BASE_DIR}')

STATIC_ROOT = BASE_DIR / 'static' #collectstatic
STATIC_URL = 'static/'
STATICFILES_DIRS = (
    BASE_DIR / '/static/' ,
)


print(f'root: {STATIC_ROOT}')
print(f'url: {STATIC_URL}')
print(f'dirs: {STATICFILES_DIRS}')
print('---------------------------------')
STATIC_ROOT = BASE_DIR / 'static' #collectstatic
STATIC_URL = 'static/'
STATICFILES_DIRS = (
    BASE_DIR / 'static/' ,
)


print(f'root: {STATIC_ROOT}')
print(f'url: {STATIC_URL}')
print(f'dirs: {STATICFILES_DIRS}')