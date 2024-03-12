#!/bin/bash

# Проверяем, установлен ли NSIS
if ! command -v makensis &> /dev/null
then
    echo "Установка NSIS"
    sudo apt-get update
    sudo apt-get install nsis
    if [ $? -eq 0 ]; then
        echo "Установка NSIS прошла успешно"
    else
        echo "Ошибка при установке NSIS"
        exit 1
    fi
fi

echo "Введите абсолютный путь к директории, где находятся DLL:"
read dll_path

target_path="src/"

# Массив с названиями DLL
dlls=("libstdc++-6.dll" "libgcc_s_seh-1.dll" "libatomic-1.dll" "libgomp-1.dll" "libssp-0.dll" "libwinpthread-1.dll")

# Массив с названиями файлов, которые нужно перенести из cmake-build-release
files_to_copy=("Main_executable.exe" "default_positions.json" "engine/libEngine_executable.dll")
cmake_build_release_path="../../cmake-build-release"

# Если src уже существует, то удалим ее
if [ -d "src" ]; then
    echo "Удаление существующей директории src"
    rm -rf src

    if [ $? -eq 0 ]; then
        echo "Удаление директории src прошло успешно"
    else
        echo "Ошибка при удалении директории src"
        exit 1
    fi
fi

# Если файл Chess_installer существует, то удалим его
if [ -f "Chess_installer.exe" ]; then
    echo "Удаление существующего файла Chess_installer.exe"
    rm Chess_installer.exe

    if [ $? -eq 0 ]; then
        echo "Удаление файла Chess_installer.exe прошло успешно"
    else
        echo "Ошибка при удалении файла Chess_installer.exe"
        exit 1
    fi
fi

# Создадим директорию src
mkdir src

# Копируем нужные файлы в src
for file in "${files_to_copy[@]}"
do
  cp "${cmake_build_release_path}/${file}" "${target_path}/"
  if [ $? -ne 0 ]; then
    echo "Ошибка при копировании файла ${file}"
    exit 1
  fi
done

for dll in "${dlls[@]}"
do
  cp "${dll_path}/${dll}" "${target_path}/"
  if [ $? -ne 0 ]; then
    echo "Ошибка при копировании файла ${dll}"
    exit 1
  fi
done

# Переименуем src/Main_executable.exe в src/chess.exe
mv src/Main_executable.exe src/chess.exe

echo "Копирование файлов прошло успешно"