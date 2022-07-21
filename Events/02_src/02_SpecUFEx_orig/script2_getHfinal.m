NAME = ['Gorner_Pt2_' datestr(now)];
diary(NAME)

load('step1_workspace')


[Name,Station,States] = insertName(2);


% homedir = '/data/tage002/tsawi/SpecUFEx/'
homedir = '/Users/theresasawi/Documents/SpecUFEx_v1/';

%where scripts are
here = [homedir Name '/02_src/02_SpecUFEx/'];



%MacOS - delete this random .DS_Store file
system('find . -name ''.DS_Store'' -type f -delete')


%reset random nuber generator
rng default






disp('This is script #2/2 for NMF')
disp(['X years of data, Station is ' Station])


file_loc = [homedir Name '/01_input/' Station '/specMats/'];

% % %
%get names of spectr files
cd(file_loc);
%MacOS - delete this random .DS_Store file
system('find . -name ''.DS_Store'' -type f -delete')
files = dir;
cd(here)

%save figures
loc_save = [homedir Name '/03_output/' Station '/SpecUFEx_output/step2_NMF/'];





[dim,num_pat] = size(W1);

h01 = 1/num_pat;
h02 = 1;
disp(Station)
disp('>>>>>>> H matrix computation')

tic;
N_batch_old = 0;
EW = W1./W2;
gain = sum(EW,1);
ElnWA = psi(W1) - log(W2) + repmat(psi(A1)-log(A2),dim,1);
NbFiles = length(files);
%for file = 1:NbFiles
 for file = 3:NbFiles
   
    %disp(['Current file is ' num2str(file) '/' num2str(NbFiles)])
    clear STFT;
    try
        load([file_loc files(file).name]);
    end
    if exist('STFT')
        X = STFT(1:dim,:);
        med = median(X(:));
        if med == 0
            med = mean(X(:)) + eps;
        end
%         X = 20*log10(X/med); # already normed etc in preprocessing
        X(X<0) = 0; %redundant
        N_batch = size(X,2);

        if N_batch ~= N_batch_old
            ElnWA_reshape = repmat(reshape(ElnWA',[num_pat 1 dim]),[1 N_batch 1]);
            t1 = max(ElnWA_reshape,[],1);
            ElnWA_reshape = ElnWA_reshape - repmat(t1,[num_pat 1 1]);
            tempMat = h02 + repmat(sum(EW.*repmat(A1./A2,dim,1),1),N_batch,1)';
            N_batch_old = N_batch;
        end

        H1 = ones(num_pat,N_batch);
        X_reshape = repmat(reshape(X',[1 N_batch dim]),[num_pat 1 1]);
        for t = 1:5
            H2 = tempMat;
            ElnH = psi(H1) - (t > 1)*log(H2);
            P = bsxfun(@plus,ElnWA_reshape,ElnH);
            P = exp(P);
            P = bsxfun(@rdivide,P,sum(P,1));
            H1 = h01 + sum(P.*X_reshape,3);
        end
        H = H1./H2;
        Xpwr = sum(X,1);
        save([loc_save 'out.' files(file).name],'H','Xpwr','gain');
        disp(['Finished ' num2str(file-2) ': ' num2str((length(files)-2-file)*(toc/(file-2))/60) ' minutes left']);
    end
end

% save dictionary and gain matrices for visualization later
save([here 'out.DictGain.mat'],'W1','gain');


save('step2_workspace')
disp('Job finished! Wow')
diary(NAME)

