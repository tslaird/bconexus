task cgp_chksum_1004 {
 File in_file

 command {
   /opt/wtsi-cgp/bin/sums2json.sh -i '${in_file}'
 }

 runtime {
   docker: "wtsicgp/dockstore-cgp-chksum:0.4.1"
 }

 output {
   File chksum_json = select_first(glob("*.check_sums.json"))
 }
}

workflow single_task {
 call cgp_chksum_1004
}