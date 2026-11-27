import shutil, sys, os
src, dst = sys.argv[1], sys.argv[2]
if not os.path.isdir(src):
    print('nothing to zip:', src); sys.exit(0)
out = shutil.make_archive(dst, 'zip', src)
print('zipped ->', os.path.abspath(out))
