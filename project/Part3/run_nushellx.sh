# Written by: Noam Gavrielov.
# Insert your directories.
directory_nushellx="/home/noam/Desktop/Physics"  # Directory in which the NushellX directory resides.
directory_isotope="isotopes"  # Directory in which the isotopes directory resides.
directory_copy="/home/noam/Desktop/Physics/PhD/courses/TALENT/course_5/2017/Talent05-Group01/project/Part3" # Directory to copy into important NushellX files.
directory_python="/home/noam/Desktop/Physics/PhD/courses/TALENT/course_5/2017/Talent05-Group01/applications"
for A in 18 19 20 21 22 23 24 25 26 27 28
do	
	# Create isotope directories in NushellX.
	#mkdir $directory_nushellx/nushellx/$directory_isotope/o${A}_usda/
	#mkdir $directory_nushellx/nushellx/$directory_isotope/o${A}_usdb/
	#echo "Create *.ans file"
	#cd $directory_python/
	#python nushellx_ans_generator.py -n o${A} -c lpe -ns 0 -ms sd -r n -i usda -pr 8 -A ${A} -j 0.0 5.5 1.0 -p 2 -op st
	#cp $directory_python/o${A}_usda.ans $directory_nushellx/nushellx/$directory_isotope/o${A}_usda/o${A}_usda.ans
	#cp $directory_python/o${A}_usdb.ans $directory_nushellx/nushellx/$directory_isotope/o${A}_usdb/o${A}_usdb.ans

	#echo "Run NushellX for" O-$A:
	#cd $directory_nushellx/nushellx/$directory_isotope/o${A}_usda/
	#shell o${A}_usda.ans
	#. o${A}_usda.bat
	#cd $directory_nushellx/nushellx/$directory_isotope/o${A}_usdb/
	#shell o${A}_usdb.ans
	#. o${A}_usdb.bat
	# Copy important files from NushellX into your own directory.
	mkdir $directory_copy/o${A}_usda/
	mkdir $directory_copy/o${A}_usda/lpe/
	mkdir $directory_copy/o${A}_usdb/
	mkdir $directory_copy/o${A}_usdb/lpe/
	cp $directory_nushellx/nushellx/$directory_isotope/o${A}_usda/o_${A}a.eps $directory_copy/o${A}_usda/o_${A}a.eps
	cp $directory_nushellx/nushellx/$directory_isotope/o${A}_usdb/o_${A}b.eps $directory_copy/o${A}_usdb/o_${A}b.eps
	
	cp $directory_nushellx/nushellx/$directory_isotope/o${A}_usda/o_${A}a.lpt $directory_copy/o${A}_usda/o_${A}a.lpt
	cp $directory_nushellx/nushellx/$directory_isotope/o${A}_usdb/o_${A}b.lpt $directory_copy/o${A}_usdb/o_${A}b.lpt

	cp $directory_nushellx/nushellx/$directory_isotope/o${A}_usda/*.lpe $directory_copy/o${A}_usda/lpe/
	cp $directory_nushellx/nushellx/$directory_isotope/o${A}_usdb/*.lpe $directory_copy/o${A}_usdb/lpe/
done

