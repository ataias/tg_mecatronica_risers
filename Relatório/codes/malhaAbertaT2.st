// k is the index of the speed vector
if dataInitialized AND k < 85 then
	MAJ(drive_axis,MAJ_1,0,speed[k],0,50.0,1,50.0,1,0,50.0,50.0,1,0,0); 
	k:=k + 1;
end_if;

if k >= 85 then
	MAS(drive_axis,MAS_1,0,0,100,1,0,100,1); 
	if MAS_1.DN then
		MSF(drive_axis,MSF_0);
	end_if;
end_if;