#!/bin/bash

function log() {
    echo "[EPFLx-RoboX-Neurorobotics (MOOC Exercises)] $*"
}

MODELS=$HBP/Models
EXPERIMENTS=$HBP/Experiments
echo
echo ----------------------------------------------------------
echo Installing EPFLx-RoboX-Neurorobotics\'s Experiments in NRP
echo ----------------------------------------------------------
echo
echo "Checking your NRP installation"
echo
echo "\$HBP: ${HBP}"
echo "\$HBP/Models: ${MODELS}"
echo "\$HBP/Experiments: ${EXPERIMENTS}"
echo

for dir in ${HBP} ${MODELS} ${EXPERIMENTS}; do
  if [[ ! -d ${dir} ]]; then
    log "The folder ${dir} doesn't exist."
    nrp_folder_not_found=1
  fi
done

nrp_info_link="https://bitbucket.org/hbpneurorobotics/neurorobotics-platform/src/master/"
if [[ ${nrp_folder_not_found} == "1" ]]; then
  log "Please check your NRP installation."
  log "All info available at ${nrp_info_link}."
  exit 1
fi

log "OK: Models, Experiments and platform_venv have been found."
echo
log "Copying models and experiment files"
echo --------------------------------------------

echo
log "Copying models into ${MODELS}"
cp -R Models/* ${HBP}/Models
echo
log "Executing \$HBP/Models/create-symlinks.sh"
bash ${MODELS}/create-symlinks.sh # Create symlinks in ~/.gazebo/models and $HBP/gzweb/http/client/assets
echo
log "Copying experiments into ${EXPERIMENTS}"
cp -R Experiments/* ${HBP}/Experiments
echo
log "Installation of EPFLx-RoboX-Neurorobotics/Models and EPFLx-RoboX-Neurorobotics/Experiments: DONE"
log "Congrats!"
