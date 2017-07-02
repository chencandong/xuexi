#!/bin/bash

usage()
{
    echo "Usage: rotate_log [-h help] [-s minsize] [-z count]
                            [-m mode] [-n detail] "
}

declare -A dic
dic=(["mode"]="move" ["n"]="no" ["minsize"]=0 ["count"]=0)


while [ $# -eq 0 ];do
    usage
    exit 0
done 

while [ $# -gt 0 ];do
  case "$1" in 
     -h) 
        usage
	exit 0
	;;
     -s) 
	shift 
	minsize=$1
	dic["minsize"]=$minsize
	shift
	;;
     -m|--mode)	
	shift
	mode=$1
	dic["mode"]=$mode
	shift
	;;
     -n)
	dic["n"]="yes"
	shift
	;;
     -z)
	shift
	count=$1
	dic["count"]=$count
	shift
	;;
     -*)
        usage
        exit 1
        ;;
      *)
	filename=$1
	dic["filename"]=$filename
	shift
	if [ $# -ne 0 ];then
	    useage
	    exit 1
	fi
	;;
   esac
done

if [ ${dic["mode"]}  !=  "move" ] &&  [ ${dic["mode"]}  !=  "copytruncate" ];then
	echo "error:mode [move|copytruncate]"
	exit 1
fi


gzipfile()
{  
  filename=$filename
  count=$count
  n=`ls|grep -c $filename`

  while [[ $n -gt $count ]]
  do
  nn=`expr $n - 1`
  if [ ! -f $filename.${nn}.gz ];then
      gzip $filename.${nn} 2>/dev/null
  else
      mv $filename.${nn}.gz  $filename.${n}.gz 2>/dev/null
  fi
  n=`expr $n - 1`
  done
  if [ -f $filename.$count ];then 
     gzip $filename.$count 
  fi
}



backupfilebymv()
{
  filename=$1
  n=`ls|grep -c $filename`

  while [[ $n -gt 1 ]]
  do
  nn=`expr $n - 1`
  mv $filename.${nn}  $filename.${n} 2>/dev/null
  n=`expr $n - 1`
  done

  if [[ $n -gt 0 ]];then
        mv $filename   ./$filename.1
        if [ $? -eq 0 ];then
           touch $filename
        fi
  fi
}

backupfilebycp()
{
  filename=$1
  n=`ls|grep -c $filename`

  while [[ $n -gt 1 ]]
  do
  nn=`expr $n - 1`
  mv $filename.${nn}  $filename.${n} 2>/dev/null
  n=`expr $n - 1`
  done

  if [[ $n -gt 0 ]];then
        cp $filename   ./$filename.1
        if [ $? -eq 0 ];then
           truncate -s 0 $filename
        fi
  fi

}

explain()
{
  filename=$1
  filesize=$2
  mode=$3
  minsize=$4
  if [[ $minsize -gt $filesize ]];then
        echo "no need to  backup"
        echo "............................."
        echo "exit the script"
        echo "............................."
  else
        echo "starting backup $filename by mode $mode"
        echo "............................."
	echo "rename $filename.n to $filename.n+1"
        echo "............................."
        if [[ $mode == "move" ]];then
	   echo "mv $filename to $filename.1"
           echo "............................."
           echo "touch new file $filename"
           echo "............................."
           echo  "successful backup $filename"
           echo "............................."
        else
           echo "cp  the $filename to $filename.n+1"
           echo "............................."
	   echo "truncate new file to size 0"
           echo "............................."
           echo  "successful backup $filename"
           echo "............................."
        fi
  fi  
}

translate()
{
   input=$1
   if [ -z "${input//[0-9]/}" ]; then
       value=${input}
   else
   lastchar=${input#${input%?}}
   num=${input%${lastchar}}
   case $lastchar in
        K|k)
        value=$(($num * 1024))
        ;;
        m|M)
        value=$(($num * 1024 * 1024))
        ;;
        g|G)
        value=$(($num * 1024 * 1024 * 1024))
        ;;
        *)
        echo "unvalid number"
        exit 1
        ;;
   esac
   fi
   echo $value
}

main()
{
   mode=${dic["mode"]}
   minsize=${dic["minsize"]}
   n=${dic["n"]}
   count=${dic["count"]}
   filename=${dic["filename"]}
   if [ ! -f  $filename ];then
      echo "no such file"
      exit 1
   fi
   echo ${dic[*]}  
 
   filesize=`ls -al |grep $filename$ |awk '{print $5}'`
   if [[ $n == "yes" ]];then
        echo "no actual command"
        echo "............................."
	explain $filename  $filesize  $mode $minsize
        exit 0
   fi
   
   if [[ $minsize == */* ]];then
      echo $minsize
      fir=`echo ${minsize%/*}`
      sed=`echo ${minsize##*/}`
      firnum=`translate $fir`
      sednum=`translate $sed`
      minsize_final=$(($firnum / $sednum))

   else
       minsize_final=`translate $minsize`
   fi

   if [[ $n == "yes" ]];then
        echo "no actual command"
        echo "............................."
        explain $filename  $filesize  $mode $minsize
        exit 0
   fi


   if [[ $minsize_final -gt $filesize ]];then
	echo "no need to  backup"
	exit 0
   else
	if [ $mode == "move" ];then
	   backupfilebymv $filename
	   echo "successful backup $filename"
	else
	   backupfilebycp $filename
	   echo "successful backup $filename"
        fi
   fi

   if [[ $count != 0 ]];then
       gzipfile $filename $count
   fi
}

main
