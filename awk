awk '{if ($0 ~ /firststring/) {found=1} if (found && $0 ~ /secondstring/) {sub(/secondstring/, "newstring"); found=0} print}' input_file > output_file
