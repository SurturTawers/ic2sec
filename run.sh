#!/bin/bash
read -p "How many times do you want to run ./main.py?: " times

for time in $(seq -w $times);
do
  python3 ./main.py > "./tmp/output_$time" &
done

echo "Waiting for executions to finish..."
wait

for time in $(seq -w $times);
do
  attacks=$(grep "Nueva poblacion: ataque"  "./tmp/output_$time" | tail -1 | sed -e 's/\(^.*\)\(.$\)/\2/');
  plot_localion=$(grep "Plot saved" "./tmp/output_$time");
  echo "Execution $time: Registered $attacks ataques. $plot_localion" 
done

echo "Output of the execution can be found in ./tmp folder."

exit 0
