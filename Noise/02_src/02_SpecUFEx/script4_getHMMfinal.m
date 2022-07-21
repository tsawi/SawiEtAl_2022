NAME = ['Gorner_Pt4_' datestr(now)];
diary(NAME)
load('step3_workspace')


[Name,Station,States] = insertName(2);


% homedir = '/data/tage002/tsawi/SpecUFEx/'
homedir = '/Users/theresasawi/Documents/SpecUFEx_v1/';

%where scripts are
here = [homedir Name '/02_src/02_SpecUFEx/'];


%MacOS - delete this .DS_Store file
system('find . -name ''.DS_Store'' -type f -delete')


%reset random number generator
rng default

% % number of clusters! Make sure you make this file, where features go
%J = 8;

disp('This is script #2/2 for HMMs')
disp(['X years of data, Station is ' Station])

%ACMs in
file_loc = [homedir Name '/03_output/' Station '/SpecUFEx_output/step2_NMF/'];
%SSout
S_loc = [homedir Name '/03_output/' Station '/SpecUFEx_output/step3_stateTransMats/'];

cd(file_loc);

%MacOS - delete this .DS_Store file
system('find . -name ''.DS_Store'' -type f -delete')

files = dir;
cd(here);
system('find . -name ''.DS_Store'' -type f -delete')

%HMM output
write_loc = [homedir Name '/03_output/' Station '/SpecUFEx_output/step4_HMM/'];
%SSout
S_loc     = [homedir Name '/03_output/' Station '/SpecUFEx_output/step4_stateTransMats/'];

%FP output
FEAT_write  = [homedir Name '/03_output/' Station '/SpecUFEx_output/step4_FEATout/'];

disp(Station)
disp('>>>>>>> final HMM computation')

[num_state,dim] = size(B1);
tauPpi = .01/num_state;
tauA = .1/num_state;
tau1 = .1;
tau2 = .1;

max_inner_ite = 20;

ElnB = psi(B1) - log(B2);
EB = B1./B2;
tic;
NbSteps = length(files)-2;
for step = 1:NbSteps
    disp(['Current step is ' num2str(step) '/' num2str(NbSteps)])
    load([file_loc files(step+2).name]);

    len_seq = size(H,2);
    H2 = diag(gain)*H;

    A = ones(num_state);
    Ppi = ones(num_state,1);

    for ite = 1:max_inner_ite
        expElnA = exp(psi(A) - repmat(psi(sum(A,2)),1,num_state));
        expElnPi = exp(psi(Ppi) - psi(sum(Ppi)));
        lnPrH = ElnB*H2 - repmat(sum(EB,2),1,len_seq);
        lnPrH = lnPrH - repmat(max(lnPrH,[],1),num_state,1);
        explnPrH = exp(lnPrH);

      % forward-backward
        alpha = zeros(num_state,len_seq);
        beta = zeros(num_state,len_seq);
        alpha(:,1) = expElnPi.*explnPrH(:,1);
        beta(:,len_seq) = 1;
        for s = 2:len_seq
            alpha(:,s) = (expElnA'*alpha(:,s-1)).*explnPrH(:,s);
            alpha(:,s) = alpha(:,s)/sum(alpha(:,s));
            beta(:,len_seq-s+1) = expElnA*(beta(:,len_seq-s+2).*explnPrH(:,len_seq-s+2));
            beta(:,len_seq-s+1) = beta(:,len_seq-s+1)/sum(beta(:,len_seq-s+1));
        end
        gam = alpha.*beta;
        gam = gam./repmat(sum(gam,1),num_state,1);
        if sum(isnan(gam(:))) > 0
            lkfsajdf lk
        end
        Ppi = tauPpi + gam(:,1);
        A = 0*A + tauA;
        for s = 2:len_seq
            mat = expElnA.*(alpha(:,s-1)*(beta(:,s).*explnPrH(:,s))');
            mat = mat/sum(mat(:));
            A = A + mat;
        end
    end
    save([S_loc files(step+2).name],'gam');

    save([write_loc files(step+2).name],'A','Ppi');
    disp(['Finished HMM ' num2str(step) ' : ' num2str((length(files)-step)*toc/(step*60)) ' minutes left']);
end

system('find . -name ''.DS_Store'' -type f -delete')

% EXTRACT FINAL FEATURE VECTORS
cd(write_loc);
system('find . -name ''.DS_Store'' -type f -delete')

files = dir;
files(1:2) = [];
% cd(here); % i think this should be commented out
system('find . -name ''.DS_Store'' -type f -delete')

T = 100;
for i = 1:length(files)
    load([write_loc files(i).name]);
    Ppi = Ppi - .01/length(Ppi);
    A = A - (.1-eps)/length(Ppi);
    Pinorm = Ppi/sum(Ppi);
    Anorm = A./repmat(sum(A,2),1,size(A,2));
%     [q,l] = eigs(Anorm',1);
%     statvec = abs(q)/sum(abs(q));
    statvec = Pinorm'*inv(eye(length(Ppi)) - T/(T+1)*Anorm)*(eye(length(Ppi)) - (T/(T+1)*Anorm)^(T+1));
    statvec = statvec'/sum(statvec);
    A2 = repmat(statvec,1,size(Anorm,2)).*(Anorm.^.5);
    save([FEAT_write files(i).name],'A2');
    disp(['Saving HMM features ' num2str(i)]);

end

cd(here);
save('EB.mat','EB')
save('ElnB.mat','ElnB')
disp('Job finished! GG, folks!')
save('step4_workspace')

diary(NAME)
%quit
