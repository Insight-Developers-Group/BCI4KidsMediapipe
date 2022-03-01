mkdir classImages
for i in $(<applicableImages)
do
   (
   mv "$i" classImages/$i
   )
done