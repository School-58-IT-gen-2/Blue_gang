#!/bin/bash

# Установим необходимые пакеты
if ! command -v unzip &> /dev/null
then
    echo "Установка unzip"
    sudo apt-get install unzip
    if [ $? -eq 0 ]; then
        echo "Установка unzip прошла успешно"
    else
        echo "Ошибка при установке unzip"
        exit 1
    fi
fi

if ! command -v jq &> /dev/null
then
    echo "Установка jq"
    sudo apt-get install jq
    if [ $? -eq 0 ]; then
        echo "Установка jq прошла успешно"
    else
        echo "Ошибка при установке jq"
        exit 1
    fi
fi

# Чтение списка репозиториев из файла dependencies.json
repos=($(jq -r '.repos[]' dependencies.json))

# Массив для хранения установленных репозиториев
installed_repos=()

if [ -d "dependencies" ]; then
    echo "Удаление существующей директории dependencies"
    rm -rf dependencies

    if [ $? -eq 0 ]; then
        echo "Удаление директории dependencies прошло успешно"
    else
        echo "Ошибка при удалении директории dependencies"
        exit 1
    fi
fi

for repo in "${repos[@]}"; do
    IFS='/' read -r -a array <<< "$repo"
    author_name="${array[0]}"
    repo_name="${array[1]}"
    branch_name="${array[2]}"

    dir_path="dependencies/$author_name/$repo_name"

    mkdir -p $dir_path
    curl -L https://github.com/$author_name/$repo_name/archive/refs/heads/$branch_name.zip --output $dir_path/$branch_name.zip
    unzip -q $dir_path/$branch_name.zip -d $dir_path
    rm $dir_path/$branch_name.zip

    if [ $? -eq 0 ]; then
        echo "Установка $repo_name прошла успешно"
        installed_repos+=("$author_name/$repo_name")
    else
        echo "Ошибка при установке $repo_name"
        exit 1
    fi
done

echo "Установленные репозитории:"
for repo in "${installed_repos[@]}"; do
    echo $repo
done