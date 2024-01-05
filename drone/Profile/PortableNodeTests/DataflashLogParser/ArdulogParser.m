fpath = '/path/to/bin/file';

log = Ardupilog(fpath);

timestamp = datetime(log.GPS.DatenumUTC,'ConvertFrom', 'datenum', 'Format', 'yyyy-MM-dd HH:mm:ss.SSSSS') - hours(4);
timestamp_str = datestr(timestamp,'yyyy-mm-dd HH:MM:SS.FFF');
ts_str = convertCharsToStrings(cellstr(timestamp_str));

% Battery generates 2 time more data than GPS logs
ix = [1 repelem(2:(size(log.GPS.Lat)/2)+1,1,2)];
ix = ix(1:end-1);

batVals = log.BAT.Volt(ix);

lineNo = 1:size(log.GPS.Lng);

exp = table(lineNo',log.GPS.Lng, log.GPS.Lat, log.GPS.Alt, batValues, ts_str, log.GPS.Status, log.GPS.NSats);


% For certain data range use the code below

% [~, start] = min(abs(timestamp - datetime('2022-05-05 15:02:34.644261')));
% [~, end] = min(abs(timestamp - datetime('2022-05-05 15:11:50.644261')));
% model = exp start end,:);
% ind1450x1450 = 1:size(model);
% model.Var1 = ind1450x1450';
% 
% writetable(model, "2022-05-05_15:02:34_vehicleOut_Regenerated.txt");