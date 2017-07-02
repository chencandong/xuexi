#!/bin/sh


#!/bin/sh
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


if [[ $1 == */* ]];then
   fir=`echo ${1%/*}`
   sed=`echo ${1##*/}`
   firnum=`translate $fir`
   sed=`translate $sed`
   finnum=$(($firnum / $sed))
   echo $finnum
else
   translate $1
fi


