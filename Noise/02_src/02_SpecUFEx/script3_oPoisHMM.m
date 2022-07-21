NAME = ['Gorner_Pt3_' datestr(now)];
diary(NAME)

load('step2_workspace')


[Name,Station,States] = insertName(2);


% homedir = '/data/tage002/tsawi/SpecUFEx/'
homedir = '/Users/theresasawi/Documents/SpecUFEx_v1/';

%where scripts are
here = [homedir Name '/02_src/02_SpecUFEx/'];





%MacOS - delete this random .DS_Store file
system('find . -name ''.DS_Store'' -type f -delete')


%reset random nuber generator
rng default



disp('This is script #1/2 for HMMs')
disp(['Station is ' Station])
file_loc = [homedir Name '/03_output/' Station '/SpecUFEx_output/step2_NMF/'];

figOut = [homedir Name '/03_output/' Station '/SpecUFEx_output/step3_NMFfigures/'];

cd(file_loc);
%MacOS - delete this random .DS_Store file
system('find . -name ''.DS_Store'' -type f -delete')

files = dir;
cd(here)

disp(Station)
disp('>>>>>>> HMM computation')

num_state = States;
tauPpi = .01/num_state;
tauA = .1/num_state;
tau1 = .1;
tau2 = .1;

max_inner_ite = 20;

%dim = 39;
testload = load([file_loc, files(3).name])
dim = length(testload.gain)

N = length(files);
n = 1;

B1 = (N/n)*1000*gamrnd(ones(num_state,dim),1);
B2 = (N/n)*1000*.03*ones(num_state,dim);

bool_sqk = 1;
NbSteps = 75000;
for step = 1:NbSteps 
    n = round(1 + 10*.75^(step-1));
    tic
    [a,b] = sort(rand(1,N));
    ElnB = psi(B1) - log(B2);
    EB = B1./B2; 
    Bup1 = zeros(size(B1));
    Bup2 = zeros(size(B2));
    Atmp = zeros(num_state);
    for i = 1:n
        [a,b] = sort(rand(1,length(files)-2));
        load([file_loc files(b(i)+2).name]);     
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
                lkfsajdf 
            end
            Ppi = tauPpi + gam(:,1);
            A = 0*A + tauA;
            for s = 2:len_seq
                mat = expElnA.*(alpha(:,s-1)*(beta(:,s).*explnPrH(:,s))');
                mat = mat/sum(mat(:));
                A = A + mat;
                if ite == max_inner_ite
                    Bup1 = Bup1 + gam(:,s)*H2(:,s)';
                    Bup2 = Bup2 + repmat(gam(:,s),1,dim);
                end
            end
        end
        Atmp = Atmp + A;
        Bup1 = Bup1 + gam(:,1)*H2(:,1)';
        Bup2 = Bup2 + repmat(gam(:,1),1,dim);
    end
    
    rho = (250/(1+5*(n-1)) + step)^-.51;
    B1 = (1-rho)*B1 + rho*(tau1 + (N/n)*Bup1);
    B2 = (1-rho)*B2 + rho*(tau2 + (N/n)*Bup2);
    
     if mod(step,100) == 0
         [a,b] = sort(sum(B1./B2,2),'descend');
         B1 = B1(b,:);
         B2 = B2(b,:);
         subplot(1,2,1); imagesc(B1./B2); colorbar; title(num2str(step));
         subplot(1,2,2); imagesc(Atmp); axis image; colorbar; pause(.01);
         timee = (NbSteps - step) * toc / 60;
         disp(['About ' num2str(timee) ' minutes remaining...'])   
         disp(['Current step is ' num2str(step) '/' num2str(NbSteps)])

     end
end


disp('Job finished! Wow')
save('step3_workspace')
diary(NAME)

