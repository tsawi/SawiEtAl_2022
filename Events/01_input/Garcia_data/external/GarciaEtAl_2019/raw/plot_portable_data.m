clear all
clf

%
% Load the bundled data from 2007 including:
%    - GPS displacement
%    - temperature
%    - lake level
%    - lake discharge
%    - calculated strain rate
%    - lake and glacier outlines
% Make quick demo figures approximately reproducing Figure 2c and Figure 4 from Garcia et al 2019
%

%
% Load the data
%
  load Bundled_data_2007.mat

%
% Strain from 2007: reproducing bits of Figure 4 from Garcia et al 2019
%
  figure(1),clf

  subplot(211)
    plot(Strain_West.Strain_time,Strain_West.E1_mag-Strain_West.E2_mag,...
         Strain_Mid.Strain_time,Strain_Mid.E1_mag-Strain_Mid.E2_mag,...
         Strain_East.Strain_time,Strain_East.E1_mag-Strain_East.E2_mag)
    xlim([165,204]),grid
    xlabel('Day of Year 2007'),ylabel('differential microstrain/day')
    legend('2007 West','2007 Mid','2007 East')

  subplot(212)
    plot(Strain_West.Strain_time,Strain_West.Rotation,...
         Strain_Mid.Strain_time,Strain_Mid.Rotation,...
         Strain_East.Strain_time,Strain_East.Rotation)
    xlim([165,204]),grid
    xlabel('Day of Year 2007'),ylabel('principal extension azimuth (ºEofN)')
    legend('2007 West','2007 Mid','2007 East')


% % Air temp, lake level, and GPS disp from 2007: reproducing bits of Figure 2c form Garcia et al 2019
% %
%   figure(2),clf


  subplot(411)
    plot(Meteor(3).time,Meteor(3).temp)
    xlim([165,204]),
    grid
    xlabel('Day of Year 2007'),ylabel('air temperature (ºC)')

  subplot(412)
    plot(LakeLevel.jday,LakeLevel.ll_2007_meters)
    xlim([165,204]),
    grid
    xlabel('Day of Year 2007'),ylabel('lake level (m)')
    
  subplot(413)
    plot(Meteor(3).time,Meteor(3).precip)
    xlim([165,204]),
    grid
    xlabel('Day of Year 2007'),ylabel('precip')
    


  subplot(4,1,3:4)
    plot(GPS_disp.jday,GPS_disp.dis-ones(length(GPS_disp.t),1)*GPS_disp.dis_on_day155,'.-')
    xlim([165,204]),grid
    xlabel('Day of Year 2007'),ylabel('Relative GPS Displacement (m)')
    legend(GPS_disp.station,'location','northwest')

%
% % Bonus: lake an
% glacier outline: reproducing bits of Figure 1 from Garcia et al 2019
% % %  
%   figure(3),clf
%   plot(Outlines.lakeshore_x,Outlines.lakeshore_y,'.-',Outlines.glac_x,Outlines.glac_y,'.-')
% 
% 

