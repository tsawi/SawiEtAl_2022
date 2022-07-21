

%Updates to all ML codes:
%
% 2021/02/18
% ~ step 4: save('ElnB.mat','ElnB')
%
%
% 2021/01/04
% ~ Removing normalization and floor (done in preprocessing) lines 101..., 115-116
% ~ also remove normalization in step 2
% ~ Line 65 script 2 :::  skip first two names: "3:NbFiles..."
%
%
% 2020/02/18
% ~ Added EB in script 4
% ~ Added script 4 saving gamma matrix, which is state trans matrix
%
% 2020/01/08
% ~ fixed path in script 5
%
% 2020/01/06
% ~ from scratch with Ben's code


NAME = ['Gorner_Pt1_' datestr(now)];
diary(NAME)


[Name,Station,States] = insertName(2);



%reset random nuber generator
rng default


% homedir = '/data/tage002/tsawi/SpecUFEx/'
homedir = '/Users/theresasawi/Documents/SpecUFEx_v1/';
%where scripts are
here = [homedir Name '/02_src/02_SpecUFEx/'];


%MacOS - delete this random .DS_Store file
system('find . -name ''.DS_Store'' -type f -delete')




disp('This is script #1/2 for NMF')
disp(['Station is ' Station])




file_loc = [homedir Name '/01_input/' Station '/specMats/'];

cd(file_loc);
files = dir;




cd(here);

disp(Station)
disp('>>>>>>> NMF computation')

dim = 266;%10000%299;%94%299 ; % 513; %308; % 308 is the length of f-vector if cut above 150 Hz (originates from the Geysers study, where there was too much noise above 150 Hz)
num_pat = 75; % number of patterns
N_eff = 100000;
N_files = 1;
P0 = 350;

h01 = 1/num_pat;
h02 = 1;

w01 = 10/dim;
w02 = 1;
W1 = (N_eff/1000)*100*(gamrnd(10*ones(dim,num_pat),1/10));
W2 = (N_eff/1000)*100*(ones(dim,num_pat));

a01 = 1/num_pat;
a02 = 1;
A1 = (N_eff/1000)*10*ones(1,num_pat);
A2 = (N_eff/1000)*10*ones(1,num_pat);

cnt_0med = 0;

NbSteps = 100000;
for step = 1:NbSteps
    tic

    T = 1 + .75^(step-1);                       % deterministic annealing temperature
    [~,t1] = sort(rand(1,length(files)-2));
    X = [];
    N_files = round(1+3*(T-1));
    i = 1;
    while i <= N_files
        clear STFT;
        try
            load([file_loc files(t1(i)+2).name]);
        end
        if exist('STFT')
            STFT = STFT(1:dim,:);
            med = median(STFT(:));
            if med == 0
                med = mean(STFT(:)) + eps;
                cnt_0med = cnt_0med + 1;
            end
%             X = [X STFT/med];
            X = [X STFT];
            i = i + 1;
        else
            i = i + 1;
            N_files = N_files + 1;
        end
        clear STFT;
    end
    P0 = 1;
%     X = floor(20*log10(X/P0)); alread done in preprocessing!
    X(X<0) = 0; % redundant; data shifted above 0

    N_batch = size(X,2);

    EW = W1./W2;
    H1 = ones(num_pat,N_batch)/num_pat;
    H2 = (h02 + repmat(sum(EW.*repmat(A1./A2,dim,1),1),N_batch,1)')/T;
    X_reshape = repmat(reshape(X',[1 N_batch dim]),[num_pat 1 1]);
    ElnWA = psi(W1) - log(W2) + repmat(psi(A1)-log(A2),dim,1);
    ElnWA_reshape = repmat(reshape(ElnWA',[num_pat 1 dim]),[1 N_batch 1]);
    t1 = max(ElnWA_reshape,[],1);
    ElnWA_reshape = ElnWA_reshape - repmat(t1,[num_pat 1 1]);
    for t = 1:10+round(1+5*(T-1))-1
        ElnH = psi(H1) - (t > 1)*log(H2);
        P = bsxfun(@plus,ElnWA_reshape/T,ElnH/T);
        P = exp(P);
        P = bsxfun(@rdivide,P,sum(P,1));
        H1 = 1 + (h01 + sum(P.*X_reshape,3) - 1)/T;
%         figure(2); imagesc(H1./H2); colorbar; pause(.1);
%         figure(2); stem(sum(W1./W2,1).*sum(H1./H2,2)'); pause(.1)
    end
    ElnH = psi(H1) - log(H2);
    P = bsxfun(@plus,ElnWA_reshape/T,ElnH/T);
    P = exp(P);
    P = bsxfun(@rdivide,P,sum(P,1));

    rho = (250/(1+5*(T-1)) + step)^-.51;

    W1_up = w01 + (N_eff/N_batch) * reshape(sum(X_reshape.*P,2),[num_pat dim])';
    W2_up = w02 + (N_eff/N_batch) * repmat(sum((H1./H2).*repmat((A1./A2)',1,N_batch),2)',dim,1);
    W1 = (1-rho)*W1 + rho*(1+(W1_up-1)/T);
    W2 = (1-rho)*W2 + rho*W2_up/T;

    A1_up = a01 + (N_eff/N_batch) * sum(sum(X_reshape.*P,3),2)';
    A2_up = a02 + (N_eff/N_batch) * (sum(W1./W2,1).*sum(H1./H2,2)');
    A1 = (1-rho)*A1 + rho*(1+(A1_up-1)/T);
    A2 = (1-rho)*A2 + rho*A2_up/T;

    idx_prune = find(A1./A2 < 10^-3);
    W1(:,idx_prune) = [];
    W2(:,idx_prune) = [];
    A1(idx_prune) = [];
    A2(idx_prune) = [];
    num_pat = length(A1);


    if sum(isnan(W1(:))) > 0 || sum(isnan(W2(:))) > 0
        lsakjfd
    end

     if mod(step,50) == 0
  	 disp(['Current step is ' num2str(step) '/' num2str(NbSteps)]);
     	 timee = (NbSteps - step) * toc / 60    ;
         disp(['Current step is ' num2str(step) '/' num2str(NbSteps)]);
         disp(['About ' num2str(timee) ' minutes remaining...'])

         figure(1);
         subplot(1,2,1); imagesc(W1./W2); colorbar; title(num2str(step));
         subplot(1,2,2); stem(A1./A2);
         pause(.1);
     end
end



disp('Job finished! Wow')
save('step1_workspace')
diary(NAME)
